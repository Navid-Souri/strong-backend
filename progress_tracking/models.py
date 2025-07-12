# progress_tracking/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone # Import timezone for default values

# فرض بر این است که TimestampedModel در core.models تعریف شده است
from core.models import TimestampedModel
# فرض بر این است که User در accounts.models تعریف شده است
from accounts.models import User

class DailyMood(TimestampedModel):
    """مدل برای ثبت حال و هوای روزانه کاربر"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_moods', verbose_name="کاربر")
    date = models.DateField(verbose_name="تاریخ") # unique=True اینجا کافی نیست، unique_together در Meta استفاده می‌شود
    mood_score = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], # 1 (بدترین) تا 5 (بهترین)
        verbose_name="امتیاز حال و هوا"
    )
    notes = models.TextField(blank=True, verbose_name="یادداشت‌ها")

    class Meta:
        verbose_name = "حال و هوای روزانه"
        verbose_name_plural = "حال و هوای روزانه"
        unique_together = ('user', 'date') # هر کاربر فقط یک حال و هوا در روز داشته باشد
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username}'s mood on {self.date}: {self.mood_score}"

class WeightLog(TimestampedModel):
    """مدل برای ثبت وزن کاربر در طول زمان"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_logs', verbose_name="کاربر")
    date = models.DateField(verbose_name="تاریخ")
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="وزن (کیلوگرم)")

    class Meta:
        verbose_name = "ثبت وزن"
        verbose_name_plural = "ثبت وزن"
        unique_together = ('user', 'date') # یک کاربر فقط یک بار در روز وزن ثبت کند
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username}'s weight on {self.date}: {self.weight_kg} kg"

class PRRecord(TimestampedModel):
    """مدل برای ثبت رکوردهای شخصی (Personal Records) کاربر برای تمرینات خاص"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pr_records', verbose_name="کاربر")
    exercise = models.ForeignKey('workouts.Exercise', on_delete=models.CASCADE, verbose_name="تمرین")
    record_date = models.DateField(verbose_name="تاریخ ثبت رکورد", default=timezone.now) # اضافه کردن مقدار پیش‌فرض
    # می‌توانید فیلدهای مختلفی برای انواع رکورد (وزن، تکرار، زمان، مسافت) داشته باشید
    max_weight_kg = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="حداکثر وزن (کیلوگرم)")
    max_reps = models.PositiveIntegerField(blank=True, null=True, verbose_name="حداکثر تکرار")
    min_time_seconds = models.PositiveIntegerField(blank=True, null=True, verbose_name="کمترین زمان (ثانیه)")
    max_distance_km = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="بیشترین مسافت (کیلومتر)")
    notes = models.TextField(blank=True, verbose_name="یادداشت‌ها")

    class Meta:
        verbose_name = "رکورد شخصی"
        verbose_name_plural = "رکوردهای شخصی"
        ordering = ['-record_date']

    def __str__(self):
        return f"{self.user.username}'s PR for {self.exercise.name} on {self.record_date}"

# مدل DailyWaterLog باید در سطح بالا و خارج از هر کلاس دیگری باشد
class DailyWaterLog(TimestampedModel):
    """مدل برای ثبت مقدار آب مصرفی روزانه"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="کاربر")
    date = models.DateField(verbose_name="تاریخ", default=timezone.now) # اضافه کردن مقدار پیش‌فرض
    amount_ml = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="مقدار آب (میلی‌لیتر)")

    class Meta:
        verbose_name = "ثبت آب روزانه"
        verbose_name_plural = "ثبت‌های آب روزانه"
        unique_together = ('user', 'date') # اطمینان از یکتا بودن هر ثبت برای هر کاربر در هر روز
        ordering = ['-date'] # مرتب‌سازی بر اساس تاریخ به صورت نزولی

    def __str__(self):
        return f"{self.user.username} - ثبت آب {self.date}: {self.amount_ml}ml"
