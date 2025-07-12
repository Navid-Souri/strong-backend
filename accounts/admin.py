# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # برای سفارشی‌سازی پنل ادمین User
from .models import User

# اگر فیلدهای اضافی به مدل User اضافه کرده‌ای، می‌تونی اینجا نمایش اونها رو در پنل ادمین کنترل کنی
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (('اطلاعات تکمیلی'), {'fields': ('is_coach', 'is_athlete', 'phone_number', 'profile_picture', 'date_of_birth', 'height_unit', 'weight_unit')}),
    )
    # اگه می‌خوای فیلدهای نمایش داده شده در لیست کاربران رو تغییر بدی:
    list_display = UserAdmin.list_display + ('is_coach', 'is_athlete', 'phone_number',)
    # اگه می‌خوای فیلدهایی رو قابل فیلتر کردن کنی:
    list_filter = UserAdmin.list_filter + ('is_coach', 'is_athlete',)


admin.site.register(User, CustomUserAdmin)