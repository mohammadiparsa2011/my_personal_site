from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='core/logo/', blank=True, null=True)
    favicon = models.ImageField(upload_to='core/favicon/', blank=True, null=True)
    default_language = models.CharField(max_length=10, default='fa')
    timezone = models.CharField(max_length=50, default='Asia/Tehran')
    short_description = models.TextField(blank=True, null=True)
    footer_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site_name

class SocialLink(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=200)
    icon_class = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class FileUpload(models.Model):
    file = models.FileField(upload_to='core/uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
    'accounts.CustomUser',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='uploaded_files'
    )

   

    def __str__(self):
        return self.file.name
