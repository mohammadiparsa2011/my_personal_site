from django.db import models
from django.utils.text import slugify
from apps.core.models import FileUpload

# -------------------------
# صفحات عمومی سایت
# -------------------------
class Page(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="عنوان صفحه"
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        allow_unicode=True,
        verbose_name="اسلاگ URL"
    )
    content = models.TextField(
        blank=True,
        verbose_name="محتوای صفحه"
    )
    cover_image = models.ForeignKey(
        FileUpload,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="تصویر شاخص"
    )

    # SEO و متادیتا
    meta_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="عنوان متا"
    )
    meta_description = models.TextField(
        blank=True,
        verbose_name="توضیحات متا"
    )
    meta_keywords = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="کلمات کلیدی متا"
    )

    # کنترل نمایش در منو یا ریدایرکت
    show_in_menu = models.BooleanField(
        default=False,
        verbose_name="نمایش در منو"
    )
    redirect_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="ریدایرکت به URL"
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
        verbose_name = "صفحه"
        verbose_name_plural = "صفحات"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
