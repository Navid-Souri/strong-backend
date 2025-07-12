# strong_app_project/accounts/views.py

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

# import کردن سریالایزرهای صحیح
from .serializers import (
    UserRegisterSerializer,
    UserSerializer, # اطمینان حاصل کنید که این UserSerializer به‌روز شده است
    MyTokenObtainPairSerializer
)
from .models import User


# ویو برای ثبت‌نام کاربر
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "ثبت نام با موفقیت انجام شد.",
            "user_id": user.id,
            "username": user.username,
        }, status=status.HTTP_201_CREATED)


# ویو برای ورود و دریافت توکن (سفارشی شده)
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ویو برای پروفایل کاربر (دریافت و ویرایش)
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer # از UserSerializer به‌روز شده استفاده می‌کند
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        # این خط را اضافه کنید تا امکان به‌روزرسانی جزئی فراهم شود
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
    