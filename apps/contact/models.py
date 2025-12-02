from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator, EmailValidator
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.core.tasks import send_contact_email_to_admin  # فرض می‌کنیم تسک Celery اینجا تعریف شده

# ------------------------------------
# وضعیت پیام (TextChoices)
# ------------------------------------
class ContactStatus(models.TextChoices):
    NEW = "new", "جدید"
    READ = "read", "خوانده شده"
    REPLIED = "replied", "پاسخ داده شده"
    ARCHIVED = "archived", "آرشیو شده"

# -------------------------
# پیام‌های فرم تماس سایت
# -------------------------
class ContactMessage(models.Model):
    # -----------------------------
    # اطلاعات ارسال‌کننده
    # -----------------------------
    full_name = models.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(3, "نام باید حداقل ۳ کاراکتر باشد."),
            RegexValidator(r'^[a-zA-Zآ-ی\s]+$', "نام فقط باید شامل حروف باشد.")
        ],
        verbose_name="نام کامل"
    )
    email = models.EmailField(
        validators=[EmailValidator(message="ایمیل وارد شده معتبر نیست.")],
        verbose_name="ایمیل"
    )
    sender_ip = models.GenericIPAddressField(
        null=True, 
        blank=True, 
        verbose_name="آدرس IP ارسال‌کننده"
    )

    # -----------------------------
    # اطلاعات پیام
    # -----------------------------
    subject = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(3, "عنوان باید حداقل ۳ کاراکتر باشد.")],
        verbose_name="عنوان پیام"
    )
    message = models.TextField(
        validators=[MinLengthValidator(10, "متن پیام باید حداقل ۱۰ کاراکتر باشد.")],
        verbose_name="متن پیام"
    )

    # -----------------------------
    # وضعیت و تاریخ‌ها
    # -----------------------------
    status = models.CharField(
        max_length=20,
        choices=ContactStatus.choices,
        default=ContactStatus.NEW,
        db_index=True,
        verbose_name="وضعیت پیام"
    )
    reply_sent_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="تاریخ ارسال پاسخ"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        indexes = [
            models.Index(fields=["status", "created_at"]),  # ایندکس ترکیبی برای جستجوی سریع
        ]

    # -----------------------------
    # متدهای کمکی
    # -----------------------------
    def mark_as_read(self):
        if self.status != ContactStatus.READ:
            self.status = ContactStatus.READ
            self.save(update_fields=["status", "updated_at"])

    def mark_as_replied(self):
        self.status = ContactStatus.REPLIED
        self.reply_sent_at = timezone.now()
        self.save(update_fields=["status", "reply_sent_at", "updated_at"])

    def mark_as_archived(self):
        self.status = ContactStatus.ARCHIVED
        self.save(update_fields=["status", "updated_at"])

    def __str__(self):
        return f"{self.full_name} - {self.subject}"

# -----------------------------
# سیگنال post_save برای اطلاع‌رسانی مدیر
# -----------------------------
@receiver(post_save, sender=ContactMessage)
def contact_message_post_save(sender, instance, created, **kwargs):
    if created:
        # فراخوانی تسک Celery برای ارسال ایمیل اطلاع‌رسانی به مدیر
        send_contact_email_to_admin.delay(instance.id)
