# -*- coding: utf-8 -*-
"""
تست‌های مدل Category
"""

import pytest
from apps.blog.models import Category

@pytest.mark.django_db  # استفاده از دیتابیس واقعی تست
class TestCategoryModel:

    def test_create_category(self):
        """تست ایجاد یک دسته‌بندی جدید"""
        category = Category.objects.create(
            title="دسته‌بندی تست",
            slug="test-category"
        )
        # بررسی مقدار فیلد title
        assert category.title == "دسته‌بندی تست"
        # بررسی مقدار فیلد slug
        assert category.slug == "test-category"
        # بررسی مقدار پیش‌فرض is_active
        assert category.is_active is True
        # بررسی خروجی __str__
        assert str(category) == "دسته‌بندی تست"

    def test_slug_uniqueness(self):
        """تست یکتایی slug"""
        Category.objects.create(title="دسته ۱", slug="unique-slug")
        with pytest.raises(Exception):
            Category.objects.create(title="دسته ۲", slug="unique-slug")
