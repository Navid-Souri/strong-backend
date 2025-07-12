"""
URL configuration for strong_app_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# strong_app_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# برای JWT Authentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# برای Routerهای DRF (برای ViewSetها)
from rest_framework.routers import DefaultRouter

# ایمپورت کردن ViewSetهای اپلیکیشن‌ها
from accounts.views import RegisterView, UserProfileView
from workouts.views import (
    ExerciseViewSet, WorkoutPlanViewSet, WorkoutPlanExerciseViewSet,
    WorkoutSessionViewSet, SetViewSet, UserWorkoutPlanAssignmentViewSet,WorkoutSummaryByDayOfWeek
)
from progress_tracking.views import DailyMoodViewSet, WeightLogViewSet, PRRecordViewSet,DailyWaterLogViewSet


# ایجاد Router برای ViewSetها
router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet)
router.register(r'workout-plans', WorkoutPlanViewSet)
router.register(r'workout-plan-exercises', WorkoutPlanExerciseViewSet)
router.register(r'workout-sessions', WorkoutSessionViewSet)
router.register(r'sets', SetViewSet)
router.register(r'user-workout-assignments', UserWorkoutPlanAssignmentViewSet)
router.register(r'daily-moods', DailyMoodViewSet)
router.register(r'weight-logs', WeightLogViewSet)
router.register(r'pr-records', PRRecordViewSet)
router.register(r'daily-water-logs', DailyWaterLogViewSet) 

urlpatterns = [
    path('admin/', admin.site.urls), # مسیر پنل ادمین
    path('api/', include(router.urls)), # مسیرهای API برای ViewSetها
    # مسیرهای احراز هویت با JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('workouts/', include('workouts.urls')),
    path('progress/', include('progress_tracking.urls')),
    # مسیرهای خاص برای کاربران (ثبت‌نام و پروفایل)
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/me/', UserProfileView.as_view(), name='user_profile'), # مسیر برای دریافت/آپدیت پروفایل کاربر فعلی
]

# اضافه کردن مسیرهای فایل‌های Media و Static در حالت توسعه
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # همچنین برای Static files در توسعه
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])