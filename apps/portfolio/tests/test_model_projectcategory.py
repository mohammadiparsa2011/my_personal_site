import pytest
from apps.portfolio.models import ProjectCategory

pytestmark = pytest.mark.django_db


def test_create_project_category():
    category = ProjectCategory.objects.create(
        title="وبسایت",
        description="پروژه های طراحی وب",
        is_active=True,
    )

    assert category.id is not None
    assert category.title == "وبسایت"
    assert category.slug == "وبسایت"
    assert category.is_active is True
    assert str(category) == "وبسایت"


def test_category_slug_auto_generate():
    category = ProjectCategory.objects.create(title="طراحی وب")
    assert category.slug == "طراحی-وب"


def test_category_unique_title():
    ProjectCategory.objects.create(title="وبسایت")
    with pytest.raises(Exception):
        ProjectCategory.objects.create(title="وبسایت")


def test_category_inactive_state():
    category = ProjectCategory.objects.create(title="غیرفعال", is_active=False)
    assert category.is_active is False