from django.test import TestCase
from apps.core.models import SiteSettings, SocialLink, FileUpload
from apps.accounts.models import CustomUser

class CoreModelsTestCase(TestCase):
    # تست ایجاد SiteSettings
    def test_create_sitesettings(self):
        """ایجاد رکورد SiteSettings و بررسی فیلدها"""
        settings = SiteSettings.objects.create(
            site_name="My Personal Site",
            short_description="یک سایت تستی",
            footer_text="Copyright 2025"
        )
        self.assertEqual(settings.site_name, "My Personal Site")
        self.assertIsNotNone(settings.created_at)

    # تست بروزرسانی SiteSettings
    def test_update_sitesettings(self):
        """بروزرسانی یک رکورد SiteSettings"""
        settings = SiteSettings.objects.create(site_name="Old Name")
        settings.site_name = "New Name"
        settings.save()
        updated = SiteSettings.objects.get(id=settings.id)
        self.assertEqual(updated.site_name, "New Name")

    # تست اعتبارسنجی SocialLink
    def test_sociallink_url_validation(self):
        """بررسی اینکه URL نامعتبر رد شود"""
        link = SocialLink(name="Invalid", url="not_a_url")
        with self.assertRaises(Exception):
            link.full_clean()  # اعتبارسنجی فیلدها

    # تست ایجاد FileUpload (بدون uploaded_by)
    def test_fileupload_create(self):
        """ایجاد رکورد FileUpload"""
        file = FileUpload.objects.create(file="path/to/file.txt")
        self.assertEqual(file.file.name, "path/to/file.txt")

    def test_file_upload_with_user(self):
        user = CustomUser.objects.create_user(email="test@example.com", username="testuser", password="pass")
        file = FileUpload.objects.create(file="dummy.txt", uploaded_by=user)
        self.assertEqual(file.uploaded_by, user)
