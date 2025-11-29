# -*- coding: utf-8 -*-
"""
تست‌های مدل Post
"""

import pytest
from django.utils import timezone
from apps.blog.models import Post, Category, Tag
from django.contrib.auth import get_user_model
from apps.core.models import FileUpload

User = get_user_model()

@pytest.mark.django_db
class TestPostModel:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
              )

    @pytest.fixture
    def category(self):
        return Category.objects.create(title="دسته تست", slug="category-test")

    @pytest.fixture
    def tag(self):
        return Tag.objects.create(title="تگ تست", slug="tag-test")

    @pytest.fixture
    def file_upload(self):
        return FileUpload.objects.create(file="dummy.jpg")  # فرضی

    def test_create_post(self, user, category, tag, file_upload):
        """تست ایجاد یک پست جدید"""
        post = Post.objects.create(
            title="پست تست",
            slug="test-post",
            summary="خلاصه تست",
            content="متن کامل پست تست",
            category=category,
            author=user,
            cover_image=file_upload,
            is_published=True,
            published_at=timezone.now()
        )
        post.tags.add(tag)
        post.save()

        assert post.title == "پست تست"
        assert post.slug == "test-post"
        assert post.summary == "خلاصه تست"
        assert post.content == "متن کامل پست تست"
        assert post.category == category
        assert post.author == user
        assert post.cover_image == file_upload
        assert post.is_published is True
        assert tag in post.tags.all()
        assert str(post) == "پست تست"

    def test_slug_uniqueness(self, user, category):
        """تست یکتایی slug برای پست"""
        Post.objects.create(
            title="پست ۱",
            slug="unique-post",
            content="متن",
            category=category,
            author=user
        )
        with pytest.raises(Exception):
            Post.objects.create(
                title="پست ۲",
                slug="unique-post",
                content="متن",
                category=category,
                author=user
            )
