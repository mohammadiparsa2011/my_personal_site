from django.db import models
from django.utils.text import slugify
from django.conf import settings
from apps.core.models import FileUpload


# -------------------------
# دسته‌بندی پروژه‌ها
# -------------------------
class ProjectCategory(models.Model):
    title = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="عنوان دسته"
    )
    slug = models.SlugField(
        unique=True,
        allow_unicode=True,
        db_index=True,
        verbose_name="اسلاگ URL"
    )
    description = models.TextField(
        blank=True,
        verbose_name="توضیحات دسته"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="فعال / غیرفعال"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# -------------------------
# تکنولوژی‌های استفاده‌شده در پروژه‌ها
# -------------------------
class Technology(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="نام تکنولوژی"
    )
    slug = models.SlugField(
        unique=True,
        allow_unicode=True,
        db_index=True,
        verbose_name="اسلاگ"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="فعال / غیرفعال"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# -------------------------
# پروژه‌ها
# -------------------------
class Project(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="عنوان پروژه"
    )
    slug = models.SlugField(
        unique=True,
        allow_unicode=True,
        db_index=True,
        verbose_name="اسلاگ"
    )
    description = models.TextField(
        blank=True,
        verbose_name="توضیح پروژه"
    )
    cover_image = models.ForeignKey(
        FileUpload,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="تصویر شاخص"
    )
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.PROTECT,
        verbose_name="دسته‌بندی"
    )
    technologies = models.ManyToManyField(
        Technology,
        blank=True,
        verbose_name="تکنولوژی‌ها"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    is_published = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="منتشر شده / نشده"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی"
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
