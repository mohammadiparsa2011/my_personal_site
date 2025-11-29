from django.db import models
from django.utils.text import slugify
from django.conf import settings
from apps.core.models import FileUpload


class Category(models.Model):
    # عنوان دسته‌بندی
    title = models.CharField(max_length=150)
    # اسلاگ برای URL، unique و ایندکس شده
    slug = models.SlugField(unique=True, db_index=True)
    # توضیحات اختیاری دسته‌بندی
    description = models.TextField(blank=True)
    # فعال/غیرفعال بودن دسته‌بندی
    is_active = models.BooleanField(default=True, db_index=True)
    # تاریخ ایجاد
    created_at = models.DateTimeField(auto_now_add=True)
    # تاریخ آخرین تغییر
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    # نام تگ
    title = models.CharField(max_length=100)
    # اسلاگ برای URL
    slug = models.SlugField(unique=True, db_index=True)
    # فعال/غیرفعال بودن تگ
    is_active = models.BooleanField(default=True, db_index=True)
    # تاریخ ایجاد
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Post(models.Model):
    # عنوان پست
    title = models.CharField(max_length=200)
    # اسلاگ برای URL
    slug = models.SlugField(unique=True, db_index=True)
    # خلاصه کوتاه پست (اختیاری)
    summary = models.CharField(max_length=300, blank=True)
    # متن کامل پست
    content = models.TextField()
    # دسته مربوط به پست
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    # تگ‌ها (چندبه‌چند)
    tags = models.ManyToManyField(Tag, blank=True)
    # نویسنده پست (کاربر)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # تصویر اصلی پست (اختیاری)
    cover_image = models.ForeignKey(FileUpload, null=True, blank=True, on_delete=models.SET_NULL)
    # وضعیت انتشار پست
    is_published = models.BooleanField(default=False, db_index=True)
    # تاریخ انتشار (اختیاری)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    # تاریخ ایجاد
    created_at = models.DateTimeField(auto_now_add=True)
    # تاریخ آخرین تغییر
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
