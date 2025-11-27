# -*- coding: utf-8 -*-
"""
این فایل شامل مدل‌های اپ Accounts است:

۱. Role: Enum برای نقش‌های کاربری
۲. CustomUser: مدل کاربر سفارشی با ایمیل به عنوان فیلد ورود
۳. CustomUserManager: مدیریت ساخت کاربر و سوپر یوزر
۴. Profile: مدل پروفایل جداگانه برای هر کاربر
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# -------------------------------
# مدل Role: تعیین نقش‌های کاربر
# -------------------------------
class Role(models.TextChoices):
    ADMIN = 'ADMIN', _('Admin')        # نقش ادمین
    USER = 'USER', _('User')           # نقش کاربر عادی
    MODERATOR = 'MOD', _('Moderator')  # نقش ناظر / مدیر محتوا

# -------------------------------
# CustomUserManager: مدیریت ایجاد کاربر
# -------------------------------
class CustomUserManager(BaseUserManager):
    """مدیریت کاربر برای ایجاد user و superuser"""

    def create_user(self, email, username, password=None, **extra_fields):
        """ساخت کاربر معمولی"""
        if not email:
            raise ValueError('ایمیل باید مشخص شود')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """ساخت سوپر یوزر با role=ADMIN"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Role.ADMIN)  # تنظیم نقش ADMIN برای سوپر یوزر

        if extra_fields.get('is_staff') is not True:
            raise ValueError('سوپر یوزر باید is_staff=True باشد')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('سوپر یوزر باید is_superuser=True باشد')

        return self.create_user(email, username, password, **extra_fields)

# -------------------------------
# مدل CustomUser: کاربر سفارشی
# -------------------------------
class CustomUser(AbstractUser):
    """مدل کاربر سفارشی با ایمیل به عنوان فیلد ورود"""
    email = models.EmailField(unique=True)  # ایمیل یکتا
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'  # ایمیل برای ورود
    REQUIRED_FIELDS = ['username']  # فیلدهای اجباری در ایجاد کاربر

    objects = CustomUserManager()  # اتصال Manager سفارشی

    def __str__(self):
        return self.email

# -------------------------------
# مدل Profile: پروفایل جداگانه برای هر کاربر
# -------------------------------
class Profile(models.Model):
    """پروفایل کاربر با ارتباط OneToOne به CustomUser"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # شماره تماس
    address = models.TextField(blank=True, null=True)                       # آدرس

    def __str__(self):
        return f"Profile of {self.user.email}"
