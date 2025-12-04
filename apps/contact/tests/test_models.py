import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.contact.models import ContactMessage


@pytest.mark.django_db
def test_create_contact_message():
    """ساخت پیام ساده باید موفق باشد"""
    msg = ContactMessage.objects.create(
        full_name="Parsa Test",
        email="test@example.com",
        subject="Hello",
        message="This is a valid test message."
    )

    assert msg.id is not None
    assert msg.status == ContactMessage.MessageStatus.NEW
    assert msg.created_at is not None
    assert msg.updated_at is not None


@pytest.mark.django_db
def test_message_validation_fail():
    """پیام کمتر از ۱۰ کاراکتر باید ولیدیشن ارور دهد"""
    msg = ContactMessage(
        full_name="Test",
        email="test@example.com",
        subject="Hi",
        message="short"
    )

    with pytest.raises(ValidationError):
        msg.full_clean()


@pytest.mark.django_db
def test_response_sets_responded_at():
    """وقتی response اضافه می‌شود responded_at باید اتوماتیک ست شود"""
    msg = ContactMessage.objects.create(
        full_name="Parsa",
        email="parsa@example.com",
        subject="Support",
        message="This is a message."
    )

    assert msg.responded_at is None

    msg.response = "Thank you for your message."
    msg.save()

    assert msg.responded_at is not None
    assert isinstance(msg.responded_at, timezone.datetime)


@pytest.mark.django_db
def test_responded_at_not_overwritten():
    """responded_at بعد از یک بار ست شدن نباید دوباره تغییر کند"""
    msg = ContactMessage.objects.create(
        full_name="Parsa",
        email="parsa@example.com",
        subject="Support",
        message="This is a message."
    )

    msg.response = "First reply"
    msg.save()

    first_time = msg.responded_at

    # تغییرات جدید نباید responded_at را عوض کند
    msg.response = "Another edit"
    msg.save()

    msg.refresh_from_db()
    assert msg.responded_at == first_time


@pytest.mark.django_db
def test_default_status_is_new():
    msg = ContactMessage.objects.create(
        full_name="Ali",
        email="ali@example.com",
        subject="Subject",
        message="Test message that is long enough."
    )
    assert msg.status == ContactMessage.MessageStatus.NEW


@pytest.mark.django_db
def test_string_representation():
    msg = ContactMessage.objects.create(
        full_name="Reza",
        email="reza@example.com",
        subject="Testing",
        message="This is a message."
    )
    assert str(msg) == "Reza — Testing"


@pytest.mark.django_db
def test_user_agent_and_ip_fields():
    msg = ContactMessage.objects.create(
        full_name="Parsa",
        email="p@example.com",
        subject="UA Test",
        message="Hello, world!",
        ip_address="127.0.0.1",
        user_agent="Mozilla/5.0 test"
    )

    assert msg.ip_address == "127.0.0.1"
    assert msg.user_agent == "Mozilla/5.0 test"


@pytest.mark.django_db
def test_response_blank_fields():
    msg = ContactMessage.objects.create(
        full_name="NoResponse",
        email="no@example.com",
        subject="No Reply",
        message="A long valid message."
    )
    assert msg.response == ""
    assert msg.responded_at is None


@pytest.mark.django_db
def test_message_update():
    msg = ContactMessage.objects.create(
        full_name="A",
        email="a@example.com",
        subject="Sub",
        message="Long enough message."
    )

    msg.message = "Updated content with enough length."
    msg.full_clean()
    msg.save()

    assert msg.message.startswith("Updated")


@pytest.mark.django_db
def test_ordering_default():
    """جدیدترین پیام باید اولین آیتم queryset باشد"""
    msg1 = ContactMessage.objects.create(
        full_name="User1",
        email="u1@example.com",
        subject="1",
        message="Msg 1 with length."
    )

    msg2 = ContactMessage.objects.create(
        full_name="User2",
        email="u2@example.com",
        subject="2",
        message="Msg 2 with length."
    )

    results = ContactMessage.objects.all()
    assert results.first() == msg2    # چون ordering = ["-created_at"]
