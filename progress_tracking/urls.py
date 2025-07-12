# progress_tracking/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    DailyMoodViewSet, DailyWaterLogViewSet, WeightLogViewSet, PRRecordViewSet, # All ViewSets
    DailyMoodSummaryLast30Days, DailyWaterSummaryLast30Days, WeightSummaryLast30Days # All Summary Views
)

router = DefaultRouter()
router.register(r'daily-moods', DailyMoodViewSet)
router.register(r'daily-water-logs', DailyWaterLogViewSet)
router.register(r'weight-logs', WeightLogViewSet)
router.register(r'pr-records', PRRecordViewSet) # New PRRecord router

urlpatterns = [
    path('', include(router.urls)),
    path('daily-mood-summary-last-30-days/', DailyMoodSummaryLast30Days.as_view(), name='daily_mood_summary_last_30_days'),
    path('daily-water-summary-last-30-days/', DailyWaterSummaryLast30Days.as_view(), name='daily_water_summary_last_30_days'),
    path('weight-summary-last-30-days/', WeightSummaryLast30Days.as_view(), name='weight_summary_last_30_days'), # New Weight Summary path
]
