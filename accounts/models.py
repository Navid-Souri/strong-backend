# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    # تعریف نقش‌های کاربر (این قسمت قبلاً در مدل شما بود)
    USER_ROLES = (
        ('user', 'User'),       # کاربر عادی / ورزشکار
        ('coach', 'Coach'),     # مربی
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='user', verbose_name='نقش کاربری')

    # اگر ایمیل رو unique کردی و خالی بودن رو اجازه نمیدی (این قسمت قبلاً در مدل شما بود)
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)

    # فیلدهای اضافی برای کاربر (قسمت‌هایی که قبلاً داشتید و تغییرات)
    is_coach = models.BooleanField(default=False, verbose_name="آیا مربی است؟")
    is_athlete = models.BooleanField(default=True, verbose_name="آیا ورزشکار است؟")
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True, verbose_name="شماره تلفن")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name="عکس پروفایل")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="تاریخ تولد")

    # فیلدهای جدید اضافه شده یا تغییر یافته برای همگام‌سازی با فرانت‌اند
    GENDER_CHOICES = (
        ('male', 'مرد'),
        ('female', 'زن'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, verbose_name="جنسیت")

    POSITION_CHOICES = (
        ('client', 'ورزشکار/مشتری'),
        ('coach', 'مربی'),
    )
    # تغییر نام فیلد role به position برای دقت بیشتر در فرم ثبت نام
    # می توانید role را نگه دارید و position را فیلد جداگانه ای در نظر بگیرید
    # اما بر اساس درخواست شما، position معادل role در فرم است.
    # من نام فیلد را به 'user_position' تغییر می دهم تا با 'role' مدل User تداخل نداشته باشد
    # و بعدا در سریالایزر آن را با role مپ می کنیم. یا می توانیم مستقیماً 'role' را استفاده کنیم
    # و 'is_coach' و 'is_athlete' را با آن همگام کنیم.
    # برای سادگی، من 'position' را به عنوان یک فیلد جدید اضافه می‌کنم.
    user_position = models.CharField(max_length=10, choices=POSITION_CHOICES, blank=True, null=True, verbose_name="نقش کاربری در اپلیکیشن")

    # وزن و قد با واحدهای جدید
    body_weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="وزن بدن")
    WEIGHT_UNIT_CHOICES = (
        ('kg', 'کیلوگرم'),
        ('lbs', 'پوند'),
    )
    weight_unit = models.CharField(max_length=5, choices=WEIGHT_UNIT_CHOICES, default='kg', blank=True, null=True, verbose_name="واحد وزن")

    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="قد")
    HEIGHT_UNIT_CHOICES = (
        ('cm', 'سانتی‌متر'),
        ('inch', 'اینچ'),
    )
    height_unit = models.CharField(max_length=5, choices=HEIGHT_UNIT_CHOICES, default='cm', blank=True, null=True, verbose_name="واحد قد")

    # فیلدهای اختصاصی برای 'client'
    gym_experience_months = models.PositiveIntegerField(blank=True, null=True, verbose_name="سابقه باشگاه (ماه)")

    # فیلدهای اختصاصی برای 'coach'
    expertise_resume = models.TextField(blank=True, null=True, verbose_name="خلاصه تخصص و سابقه")
    license = models.CharField(max_length=100, blank=True, null=True, verbose_name="مجوز/گواهی‌نامه")
    license_number = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name="شماره مجوز")

    # اندازه‌گیری‌های بدن
    neck_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="دور گردن")
    shoulder_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="دور شانه")
    arm_r_biceps_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="دور بازوی راست (بایسپس)")
    arm_r_triceps_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="دور بازوی راست (ترایسپس)")
    arm_l_biceps_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="دور بازوی چپ (بایسپس)")
    arm_l_triceps_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="دور بازوی چپ (ترایسپس)")
    chest_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="دور سینه")
    under_chest_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="دور زیر سینه (فقط برای خانم‌ها)")
    waist_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="دور کمر")
    abdomen_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="دور شکم")
    hip_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="دور باسن")
    thigh_r_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="دور ران راست")
    thigh_l_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="دور ران چپ")
    calves_r_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="دور ساق پای راست")
    calves_l_size = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="دور ساق پای چپ")

    # می‌توانید فیلدهای دیگر AbstractUser را هم override کنید
    # مثلاً اگر نمی‌خواهید از username استفاده کنید و می‌خواهید ایمیل را به عنوان USERNAME_FIELD قرار دهید:
    # EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = ['email'] # اگر username را حذف کنید، باید ایمیل را اینجا بگذارید
    # username = None # اگر می‌خواهید username را حذف کنید، این خط را اضافه کنید