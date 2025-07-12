# workouts/views.py
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum, F # Added F
from django.db.models.functions import ExtractWeekDay, ExtractMonth, ExtractYear
from django.utils import timezone
from datetime import timedelta

from accounts.models import User 

from .models import Exercise, WorkoutPlan, WorkoutSession, Set, UserWorkoutPlanAssignment, WorkoutPlanExercise
from .serializers import (
    ExerciseSerializer, WorkoutPlanSerializer, WorkoutSessionSerializer,
    SetSerializer, UserWorkoutPlanAssignmentSerializer, WorkoutPlanExerciseSerializer
)

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class WorkoutPlanExerciseViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlanExercise.objects.all()
    serializer_class = WorkoutPlanExerciseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class WorkoutSessionViewSet(viewsets.ModelViewSet):
    queryset = WorkoutSession.objects.all()
    serializer_class = WorkoutSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SetViewSet(viewsets.ModelViewSet):
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Set.objects.filter(workout_session__user=self.request.user)
        workout_session_id = self.request.query_params.get('session_id', None)
        if workout_session_id is not None:
            queryset = queryset.filter(workout_session__id=workout_session_id)
        return queryset.order_by('set_number')

class UserWorkoutPlanAssignmentViewSet(viewsets.ModelViewSet):
    queryset = UserWorkoutPlanAssignment.objects.all()
    serializer_class = UserWorkoutPlanAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_coach:
            return UserWorkoutPlanAssignment.objects.filter(assigned_by=self.request.user)
        elif self.request.user.is_athlete:
            return UserWorkoutPlanAssignment.objects.filter(user=self.request.user)
        return UserWorkoutPlanAssignment.objects.none()

    def perform_create(self, serializer):
        if self.request.user.is_coach:
            serializer.save(assigned_by=self.request.user)
        else:
            raise permissions.ValidationError("Only coaches can assign workout plans.")

class WorkoutSummaryByDayOfWeek(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        unique_exercises_counts = Set.objects.filter(
            workout_session__user=request.user
        ).annotate(
            day_of_week=ExtractWeekDay('workout_session__date')
        ).values('day_of_week').annotate(
            total_unique_exercises=Count('exercise', distinct=True)
        ).order_by('day_of_week')

        day_names_fa = {
            1: 'یکشنبه', 2: 'دوشنبه', 3: 'سه‌شنبه', 4: 'چهارشنبه',
            5: 'پنج‌شنبه', 6: 'جمعه', 7: 'شنبه'
        }

        result = []
        for item in unique_exercises_counts:
            result.append({
                'day': day_names_fa.get(item['day_of_week'], 'نامشخص'),
                'total_unique_exercises': item['total_unique_exercises']
            })

        return Response(result)

class WorkoutSummaryByMonth(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        unique_exercises_counts = Set.objects.filter(
            workout_session__user=request.user
        ).annotate(
            month=ExtractMonth('workout_session__date'),
            year=ExtractYear('workout_session__date')
        ).values('year', 'month').annotate(
            total_unique_exercises=Count('exercise', distinct=True)
        ).order_by('year', 'month')

        month_names_en = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }

        result = []
        for item in unique_exercises_counts:
            result.append({
                'month_year': f"{month_names_en.get(item['month'], 'Unknown')} {item['year']}",
                'exercises': item['total_unique_exercises']
            })

        return Response(result)

class WorkoutSummaryLast30Days(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        today = timezone.localdate()
        thirty_days_ago = today - timedelta(days=29) # Include today and 29 previous days

        # CORRECTED: Use 'workout_session__date' directly in .values()
        # as it's already a DateField, no need for models.DateField(models.F(...))
        unique_exercises_counts = Set.objects.filter(
            workout_session__user=request.user,
            workout_session__date__gte=thirty_days_ago,
            workout_session__date__lte=today
        ).values('workout_session__date').annotate( # Changed this line
            total_unique_exercises=Count('exercise', distinct=True)
        ).order_by('workout_session__date') # And this line to match

        # Create a dictionary for quick lookup of existing data
        # Ensure the key matches the field name used in .values()
        data_map = {item['workout_session__date'].strftime('%Y-%m-%d'): item['total_unique_exercises']
                    for item in unique_exercises_counts}

        # Generate data for all 30 days, filling in 0 for days with no workouts
        result = []
        for i in range(30):
            current_date = thirty_days_ago + timedelta(days=i)
            date_str = current_date.strftime('%Y-%m-%d')
            result.append({
                'date': date_str,
                'exercises': data_map.get(date_str, 0)
            })

        return Response(result)

    