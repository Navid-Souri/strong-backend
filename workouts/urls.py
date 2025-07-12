# workouts/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    ExerciseViewSet, WorkoutPlanViewSet, WorkoutSessionViewSet, SetViewSet,
    UserWorkoutPlanAssignmentViewSet, WorkoutPlanExerciseViewSet,WorkoutSummaryByMonth,
    WorkoutSummaryByDayOfWeek,WorkoutSummaryLast30Days # اضافه کردن ویو جدید
)

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet)
router.register(r'workout-plans', WorkoutPlanViewSet)
router.register(r'workout-plan-exercises', WorkoutPlanExerciseViewSet) # مسیر برای مدل واسط
router.register(r'workout-sessions', WorkoutSessionViewSet)
router.register(r'sets', SetViewSet)
router.register(r'user-assignments', UserWorkoutPlanAssignmentViewSet)

# router.register(r'daily-moods', DailyMoodViewSet) # اگر اینها را فعال کردید، مطمئن شوید که ViewSet مربوطه را import کرده‌اید
# router.register(r'weight-logs', WeightLogViewSet)
# router.register(r'pr-records', PRRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # اضافه کردن مسیر برای ویو جدید
    path('workout-summary-by-day/', WorkoutSummaryByDayOfWeek.as_view(), name='workout_summary_by_day_of_week'),
    path('workout-summary-by-month/', WorkoutSummaryByMonth.as_view(), name='workout_summary_by_month'), # NEW: Path for monthly summary
    path('workout-summary-last-30-days/', WorkoutSummaryLast30Days.as_view(), name='workout_summary_last_30_days'), # NEW: Path for 30-day summary
]
