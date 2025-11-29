# -*- coding: utf-8 -*-
"""
تست‌های مدل Tag
"""

import pytest
from apps.blog.models import Tag

@pytest.mark.django_db
class TestTagModel:

    def test_create_tag(self):
        """تست ایجاد یک تگ جدید"""
        tag = Tag.objects.create(title="تگ تست", slug="test-tag")
        assert tag.title == "تگ تست"
        assert tag.slug == "test-tag"
        assert tag.is_active is True
        assert str(tag) == "تگ تست"

    def test_slug_uniqueness(self):
        """تست یکتایی slug در تگ"""
        Tag.objects.create(title="تگ ۱", slug="unique-tag")
        with pytest.raises(Exception):
            Tag.objects.create(title="تگ ۲", slug="unique-tag")
