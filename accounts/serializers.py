# strong_app_project/accounts/serializers.py

from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2', 'first_name', 'last_name',
            'phone_number', 'body_weight', 'weight_unit', 'height', 'height_unit',
            'gender', 'user_position', # 'user_position' به جای 'position' در مدل ما
            'gym_experience_months', 'expertise_resume', 'license', 'license_number',
            'neck_size', 'shoulder_size', 'arm_r_biceps_size', 'arm_r_triceps_size',
            'arm_l_biceps_size', 'arm_l_triceps_size', 'chest_size', 'under_chest_size',
            'waist_size', 'abdomen_size', 'hip_size',
            'thigh_r_size', 'thigh_l_size', 'calves_r_size', 'calves_l_size',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        user_position = attrs.get('user_position') # نام فیلد در مدل
        gender = attrs.get('gender')

        # اعتبار سنجی فیلدهای شرطی بر اساس 'position'
        if user_position == 'client':
            if not attrs.get('gym_experience_months'):
                raise serializers.ValidationError({"gym_experience_months": "سابقه باشگاه برای ورزشکار الزامی است."})
        elif user_position == 'coach':
            if not attrs.get('expertise_resume'):
                raise serializers.ValidationError({"expertise_resume": "خلاصه تخصص و سابقه برای مربی الزامی است."})
            if not attrs.get('license'):
                raise serializers.ValidationError({"license": "مجوز/گواهی‌نامه برای مربی الزامی است."})
            if not attrs.get('license_number'):
                raise serializers.ValidationError({"license_number": "شماره مجوز برای مربی الزامی است."})
        elif not user_position: # اگر position انتخاب نشده باشد
             raise serializers.ValidationError({"user_position": "نقش کاربری الزامی است."})

        # اعتبار سنجی فیلدهای اندازه‌گیری اصلی (همه را الزامی می‌کنیم همانطور که در فرانت‌اند `required` شده‌اند)
        required_measurements = [
            'body_weight', 'weight_unit', 'height', 'height_unit', 'gender',
            'neck_size', 'shoulder_size', 'arm_r_biceps_size', 'arm_r_triceps_size',
            'arm_l_biceps_size', 'arm_l_triceps_size', 'chest_size', 'waist_size',
            'abdomen_size', 'hip_size', 'thigh_r_size', 'thigh_l_size',
            'calves_r_size', 'calves_l_size',
        ]
        for field in required_measurements:
            if not attrs.get(field):
                raise serializers.ValidationError({field: f"فیلد '{field}' الزامی است."})

        # اعتبار سنجی فیلد 'under_chest_size' فقط برای خانم‌ها
        if gender == 'female' and not attrs.get('under_chest_size'):
            raise serializers.ValidationError({"under_chest_size": "دور زیر سینه برای بانوان الزامی است."})
        # اگر جنسیت مرد است، مطمئن می‌شویم این فیلد وجود نداشته باشد یا خالی باشد
        if gender == 'male' and attrs.get('under_chest_size') is not None:
             raise serializers.ValidationError({"under_chest_size": "فیلد دور زیر سینه فقط برای بانوان است."})


        return attrs

    def create(self, validated_data):
        # حذف password2 قبل از ایجاد کاربر
        validated_data.pop('password2')

        # تعیین نقش کاربر بر اساس 'user_position'
        user_position = validated_data.pop('user_position', None)
        if user_position == 'coach':
            validated_data['role'] = 'coach'
            validated_data['is_coach'] = True
            validated_data['is_athlete'] = False # مربی ورزشکار عادی نیست
        elif user_position == 'client':
            validated_data['role'] = 'user' # نقش 'user' در مدل به معنای ورزشکار عادی
            validated_data['is_coach'] = False
            validated_data['is_athlete'] = True


        user = User.objects.create_user(**validated_data)
        return user

# <--- این کلاس از UserProfileSerializer به UserSerializer تغییر نام یافته است!
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'role',
            'phone_number', 'body_weight', 'weight_unit', 'height', 'height_unit',
            'gender', 'user_position',
            'gym_experience_months', 'expertise_resume', 'license', 'license_number',
            'neck_size', 'shoulder_size', 'arm_r_biceps_size', 'arm_r_triceps_size',
            'arm_l_biceps_size', 'arm_l_triceps_size', 'chest_size', 'under_chest_size',
            'waist_size', 'abdomen_size', 'hip_size',
            'thigh_r_size', 'thigh_l_size', 'calves_r_size', 'calves_l_size',
            'is_coach', 'is_athlete', 'date_joined' # اضافه کردن این فیلدها برای نمایش
        ]
        read_only_fields = [
            'id', 'role', 'user_position', 'is_coach', 'is_athlete', 'date_joined',
            'gym_experience_months', 'expertise_resume', 'license', 'license_number',
            # این فیلدها معمولا توسط کاربر ویرایش نمی‌شوند، اما اگر نیاز بود می‌توان آن‌ها را از اینجا حذف کرد.
            'neck_size', 'shoulder_size', 'arm_r_biceps_size', 'arm_r_triceps_size',
            'arm_l_biceps_size', 'arm_l_triceps_size', 'chest_size', 'under_chest_size',
            'waist_size', 'abdomen_size', 'hip_size',
            'thigh_r_size', 'thigh_l_size', 'calves_r_size', 'calves_l_size',
        ]


# --------------------------------------------------------------------------------
# این کلاس MyTokenObtainPairSerializer بدون تغییر باقی می ماند
# --------------------------------------------------------------------------------
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializerr سفارشی برای JWT.
    میتونی فیلدهای بیشتری رو به پاسخ توکن اضافه کنی،
    مثلا نقش کاربر رو اینجا برگردونی.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # اضافه کردن فیلدهای سفارشی به توکن
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role # اضافه کردن نقش کاربری به توکن
        token['user_position'] = user.user_position # اضافه کردن نقش کاربری به توکن

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # اگر می‌خواهی نقش رو در پاسخ لاگین هم برگردونی (نه فقط در توکن)
        data['role'] = self.user.role
        data['user_position'] = self.user.user_position # اضافه کردن به پاسخ ورود
        return data
