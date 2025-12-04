from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class ContactMessage(models.Model):
    # اطلاعات فرستنده
    full_name = models.CharField(
        max_length=150,
        verbose_name="نام و نام خانوادگی"
    )
    email = models.EmailField(
        verbose_name="ایمیل"
    )
    subject = models.CharField(
        max_length=200,
        verbose_name="عنوان پیام"
    )
    message = models.TextField(
        verbose_name="متن پیام"
    )

    # پاسخ مدیر سایت
    response = models.TextField(
        blank=True,
        verbose_name="پاسخ مدیر"
    )
    responded_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="زمان پاسخ‌گویی"
    )

    # وضعیت پیام
    class MessageStatus(models.TextChoices):
        NEW = "new", "جدید"
        READ = "read", "دیده شده"
        ANSWERED = "answered", "پاسخ داده شده"
        ARCHIVED = "archived", "آرشیوشده"

    status = models.CharField(
        max_length=20,
        choices=MessageStatus.choices,
        default=MessageStatus.NEW,
        db_index=True,
        verbose_name="وضعیت پیام"
    )

    # اطلاعات امنیتی
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="آدرس IP"
    )
    user_agent = models.CharField(
        max_length=1000,  # افزایش طول طبق پیشنهاد
        blank=True,
        verbose_name="User Agent"
    )

    # زمان‌ها
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ارسال"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی"
    )

    # متادیتا
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        indexes = [
            models.Index(fields=["email", "status"]),
            models.Index(fields=["created_at"]),
        ]

    # ولیدیشن
    def clean(self):
        if self.message and len(self.message.strip()) < 10:
            raise ValidationError("متن پیام باید حداقل ۱۰ کاراکتر باشد.")

    # رفتار پاسخ‌دهی
    def save(self, *args, **kwargs):
        if self.response and not self.responded_at:
            self.responded_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} — {self.subject}"
