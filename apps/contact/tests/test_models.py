import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.contact.models import ContactMessage, ContactStatus
from unittest.mock import patch

pytestmark = pytest.mark.django_db

# مسیر Celery Task برای Mock (فقط متد delay)
CELERY_TASK_PATH = "apps.contact.models.send_contact_email_to_admin"

# ----------------------------------------------------------------------
# تابع کمکی برای ایجاد پیام معتبر
# ----------------------------------------------------------------------
def create_message():
    return ContactMessage.objects.create(
        full_name="Ali",
        email="ali@example.com",
        subject="Hello",
        message="This is a test message with 32 characters."
    )

# -----------------------------
# تست‌های اعتبارسنجی فیلدها
# -----------------------------
@patch(f"{CELERY_TASK_PATH}.delay")  # فقط delay را Mock می‌کنیم
def test_full_name_validation(mock_delay):
    msg = create_message()
    with pytest.raises(ValidationError):
        msg.full_name = ""
        msg.full_clean()

@patch(f"{CELERY_TASK_PATH}.delay")
def test_email_validation(mock_delay):
    msg = create_message()
    with pytest.raises(ValidationError):
        msg.email = "invalid_email"
        msg.full_clean()

@patch(f"{CELERY_TASK_PATH}.delay")
def test_message_length_validation(mock_delay):
    msg = create_message()
    with pytest.raises(ValidationError):
        msg.message = "short"
        msg.full_clean()

# -----------------------------
# تست متدهای کمکی تغییر وضعیت
# -----------------------------
@patch(f"{CELERY_TASK_PATH}.delay")
def test_mark_as_read(mock_delay):
    msg = create_message()
    mock_delay.reset_mock()
    assert msg.status == ContactStatus.NEW
    msg.mark_as_read()
    msg.refresh_from_db()
    assert msg.status == ContactStatus.READ
    mock_delay.assert_not_called()

@patch(f"{CELERY_TASK_PATH}.delay")
def test_mark_as_replied(mock_delay):
    msg = create_message()
    mock_delay.reset_mock()
    msg.mark_as_replied()
    msg.refresh_from_db()
    assert msg.status == ContactStatus.REPLIED
    assert msg.reply_sent_at is not None
    assert isinstance(msg.reply_sent_at, timezone.datetime)
    mock_delay.assert_not_called()

@patch(f"{CELERY_TASK_PATH}.delay")
def test_mark_as_archived(mock_delay):
    msg = create_message()
    mock_delay.reset_mock()
    msg.mark_as_archived()
    msg.refresh_from_db()
    assert msg.status == ContactStatus.ARCHIVED
    mock_delay.assert_not_called()

@patch(f"{CELERY_TASK_PATH}.delay")
def test_mark_as_read_preserves_other_fields(mock_delay):
    initial_ip = "192.168.1.1"
    initial_reply_time = timezone.now() - timezone.timedelta(hours=1)
    
    msg = ContactMessage.objects.create(
        full_name="Ali",
        email="ali@example.com",
        subject="Test",
        message="Message content here",
        sender_ip=initial_ip,
        reply_sent_at=initial_reply_time,
        status=ContactStatus.NEW
    )
    mock_delay.reset_mock()
    
    msg.mark_as_read()
    msg.refresh_from_db()
    assert msg.sender_ip == initial_ip
    assert msg.reply_sent_at == initial_reply_time
    mock_delay.assert_not_called()

# -----------------------------
# تست سیگنال post_save و فراخوانی Celery
# -----------------------------
@patch(f"{CELERY_TASK_PATH}.delay")
def test_post_save_signal_calls_celery_task(mock_delay):
    msg = create_message()
    # وقتی پیام ساخته می‌شود، post_save باید delay را صدا بزند
    mock_delay.assert_called_once_with(msg.id)

@patch(f"{CELERY_TASK_PATH}.delay")
def test_post_save_signal_does_not_call_on_update(mock_delay):
    msg = create_message()
    mock_delay.reset_mock()
    msg.mark_as_read()  # save با created=False
    mock_delay.assert_not_called()
