import pytest
from apps.portfolio.models import Technology

pytestmark = pytest.mark.django_db


def test_create_technology():
    tech = Technology.objects.create(name="Python", is_active=True)

    assert tech.id is not None
    assert tech.name == "Python"
    assert tech.slug == "python"
    assert tech.is_active is True
    assert str(tech) == "Python"


def test_technology_slug_auto_generate():
    tech = Technology.objects.create(name="جاوا اسکریپت")
    assert tech.slug == "جاوا-اسکریپت"


def test_technology_unique_name():
    Technology.objects.create(name="Django")
    with pytest.raises(Exception):
        Technology.objects.create(name="Django")


def test_technology_inactive_state():
    tech = Technology.objects.create(name="Rust", is_active=False)
    assert tech.is_active is False