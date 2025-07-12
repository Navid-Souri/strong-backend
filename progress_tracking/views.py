# progress_tracking/views.py
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum, F
from django.utils import timezone
from datetime import timedelta

from .models import DailyMood, DailyWaterLog, WeightLog, PRRecord # Removed WaterIntake
from .serializers import (
    DailyMoodSerializer,
    DailyWaterLogSerializer,
    WeightLogSerializer,
    PRRecordSerializer # Added PRRecordSerializer
)

class BaseProgressViewSet(viewsets.ModelViewSet):
    """Base ViewSet for progress tracking models"""
    permission_classes = [permissions.IsAuthenticated]
    ordering = ['-date'] # Default ordering, can be overridden by subclasses

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by(*self.ordering)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DailyMoodViewSet(BaseProgressViewSet):
    queryset = DailyMood.objects.all()
    serializer_class = DailyMoodSerializer

class DailyWaterLogViewSet(BaseProgressViewSet):
    queryset = DailyWaterLog.objects.all()
    serializer_class = DailyWaterLogSerializer

class WeightLogViewSet(BaseProgressViewSet):
    queryset = WeightLog.objects.all()
    serializer_class = WeightLogSerializer

class PRRecordViewSet(BaseProgressViewSet): # New ViewSet for PRRecord
    queryset = PRRecord.objects.all()
    serializer_class = PRRecordSerializer
    ordering = ['-record_date'] # PRs are ordered by record_date

class BaseSummaryLast30Days(APIView):
    """Base class for 30-day summary views"""
    permission_classes = [permissions.IsAuthenticated]
    model = None
    date_field = 'date'
    value_field = None
    default_value = 0 # Default value for days with no data

    def get(self, request, format=None):
        today = timezone.localdate()
        thirty_days_ago = today - timedelta(days=29)

        data = self.model.objects.filter(
            user=request.user,
            **{f'{self.date_field}__gte': thirty_days_ago,
               f'{self.date_field}__lte': today}
        ).values(self.date_field, self.value_field).order_by(self.date_field)

        data_map = {item[self.date_field].strftime('%Y-%m-%d'): item[self.value_field]
                    for item in data}

        result = []
        for i in range(30):
            current_date = thirty_days_ago + timedelta(days=i)
            date_str = current_date.strftime('%Y-%m-%d')
            result.append({
                'date': date_str,
                self.value_field: data_map.get(date_str, self.default_value)
            })
        return Response(result)

class DailyMoodSummaryLast30Days(BaseSummaryLast30Days):
    model = DailyMood
    value_field = 'mood_score' # CORRECTED: Changed from 'mood_rating' to 'mood_score'
    default_value = None # Using None for mood as 0 might be misleading for a rating scale

class DailyWaterSummaryLast30Days(BaseSummaryLast30Days):
    model = DailyWaterLog
    value_field = 'amount_ml'
    default_value = 0 # Water intake can reasonably be 0

class WeightSummaryLast30Days(BaseSummaryLast30Days):
    model = WeightLog
    value_field = 'weight_kg'
    default_value = None # Using None for weight as 0 might be misleading
