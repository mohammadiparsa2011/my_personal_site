# -*- coding: utf-8 -*-
"""
تست‌های اپ Accounts:

۱. تست ساخت کاربر معمولی
۲. تست ساخت سوپر یوزر با role=ADMIN
۳. تست ساخت پروفایل مرتبط با کاربر
"""

from django.test import TestCase
from apps.accounts.models import CustomUser, Profile, Role

# -------------------------------
# تست مدل CustomUser
# -------------------------------
class CustomUserModelTest(TestCase):

    def test_create_user(self):
        """تست ایجاد کاربر معمولی"""
        user = CustomUser.objects.create_user(
            username='parsa',
            email='parsa@test.com',
            password='123456'
        )
        self.assertEqual(user.email, 'parsa@test.com')
        self.assertEqual(user.role, Role.USER)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """تست ایجاد سوپر یوزر"""
        admin = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='123456'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertEqual(admin.role, Role.ADMIN)

# -------------------------------
# تست مدل Profile
# -------------------------------
class ProfileModelTest(TestCase):

    def test_profile_creation(self):
        """تست ایجاد پروفایل برای کاربر"""
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='123'
        )
        profile = Profile.objects.create(
            user=user,
            phone_number='09123456789',
            address='Tehran, Iran'
        )
        self.assertEqual(profile.user.email, 'test@test.com')
        self.assertEqual(profile.phone_number, '09123456789')
        self.assertEqual(profile.address, 'Tehran, Iran')
        self.assertEqual(str(profile), f"Profile of {user.email}")
