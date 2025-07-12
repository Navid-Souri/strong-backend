# core/models.py
from django.db import models

class TimestampedModel(models.Model):
    """
    یک مدل انتزاعی که فیلدهای created_at و updated_at را به صورت خودکار اضافه می‌کند.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    class Meta:
        abstract = True # این مدل یک جدول در دیتابیس ایجاد نمی‌کند
        ordering = ['-created_at'] # مرتب‌سازی پیش‌فرض بر اساس تاریخ ایجاد (جدیدترین اول)