import pytest
from django.utils.text import slugify
from apps.pages.models import Page
from apps.core.models import FileUpload
from apps.accounts.models import CustomUser

# -------------------------
# Fixtures
# -------------------------
@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(
        email="test@example.com",
        username="tester",
        password="pass1234"
    )

@pytest.fixture
def file_upload(user):
    return FileUpload.objects.create(
        file="uploads/test_file.txt",
        uploaded_by=user
    )

@pytest.fixture
def page(file_upload):
    return Page.objects.create(
        title="صفحه تستی",
        content="<p>محتوای HTML تست</p>",
        cover_image=file_upload,
        meta_title="عنوان متای تست",
        meta_description="توضیحات متای تست",
        meta_keywords="django, test, page",
        show_in_menu=True,
        redirect_url="https://example.com"
    )

# -------------------------
# Tests
# -------------------------
@pytest.mark.django_db
def test_page_creation(page, file_upload):
    assert page.title == "صفحه تستی"
    assert page.content == "<p>محتوای HTML تست</p>"
    assert page.cover_image == file_upload
    assert page.is_published is True
    assert page.show_in_menu is True
    assert page.redirect_url == "https://example.com"
    assert page.meta_title == "عنوان متای تست"
    assert page.meta_description == "توضیحات متای تست"
    assert page.meta_keywords == "django, test, page"

@pytest.mark.django_db
def test_slug_autogeneration(page):
    assert page.slug == slugify("صفحه تستی", allow_unicode=True)

@pytest.mark.django_db
def test_str_method(page):
    assert str(page) == page.title

@pytest.mark.django_db
def test_update_page_content(page):
    page.content = "<p>محتوای جدید</p>"
    page.save()
    page.refresh_from_db()
    assert page.content == "<p>محتوای جدید</p>"

@pytest.mark.django_db
def test_ordering(page):
    new_page = Page.objects.create(title="صفحه جدید")
    pages = Page.objects.all()
    assert pages.first() == new_page
    assert pages.last() == page

@pytest.mark.django_db
def test_redirect_and_menu_fields(page):
    page.redirect_url = "https://example.org"
    page.show_in_menu = False
    page.save()
    page.refresh_from_db()
    assert page.redirect_url == "https://example.org"
    assert page.show_in_menu is False