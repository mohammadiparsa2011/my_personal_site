import pytest
from django.contrib.auth import get_user_model
from apps.portfolio.models import Project, ProjectCategory, Technology

pytestmark = pytest.mark.django_db
User = get_user_model()


def test_project_creation_with_minimal_fields():
    user = User.objects.create_user(email="test@example.com", username="testuser", password="12345")
    category = ProjectCategory.objects.create(title="برنامه نویسی")

    project = Project.objects.create(
        title="پروژه تستی",
        category=category,
        author=user,
    )

    assert project.id is not None
    assert project.slug == "پروژه-تستی"
    assert project.category == category
    assert project.author == user
    assert str(project) == "پروژه تستی"


def test_project_associates_multiple_technologies():
    user = User.objects.create_user(email="t2@example.com", username="u2", password="12345")
    category = ProjectCategory.objects.create(title="طراحی سایت")

    tech1 = Technology.objects.create(name="Python")
    tech2 = Technology.objects.create(name="Django")

    project = Project.objects.create(title="سایت شرکتی", category=category, author=user)
    project.technologies.add(tech1, tech2)

    assert project.technologies.count() == 2
    assert tech1 in project.technologies.all()
    assert tech2 in project.technologies.all()


def test_project_ordering_by_created_at():
    user = User.objects.create_user(email="order@example.com", username="orderuser", password="12345")
    category = ProjectCategory.objects.create(title="دسته تست")

    p1 = Project.objects.create(title="اول", category=category, author=user)
    p2 = Project.objects.create(title="دوم", category=category, author=user)

    projects = Project.objects.all()
    assert projects[0] == p2
    assert projects[1] == p1


def test_project_category_protect_delete():
    user = User.objects.create_user(email="protect@example.com", username="protectuser", password="12345")
    category = ProjectCategory.objects.create(title="دسته محافظت شده")

    Project.objects.create(title="پروژه", category=category, author=user)

    with pytest.raises(Exception):
        category.delete()