import hashlib

from django.db import models

from main import ndutils


class PageUrl(models.Model):
    url = models.URLField(null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_polled_on = models.DateTimeField(null=True)
    last_parsed_on = models.DateTimeField(null=True)
    last_change_on = models.DateTimeField(null=True)  # last text change detected
    last_error_on = models.DateTimeField(null=True)
    last_error_description = models.CharField(max_length=100, default="")

    @property
    def count_texts(self):
        return self.texts.count()

    def __str__(self):
        return self.url


class PageText(models.Model):
    url = models.ForeignKey(PageUrl, on_delete=models.CASCADE, related_name="texts")
    created_on = models.DateTimeField(auto_now_add=True)

    html = models.TextField(default="")
    html_hashed = models.CharField(max_length=32, default="")
    is_html_changed = models.BooleanField(default=True)

    text = models.TextField(default="")
    text_hashed = models.CharField(max_length=32, default="")
    is_text_changed = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.html_hashed = ndutils.get_hash(self.html)
        self.text_hashed = ndutils.get_hash(self.text)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.url.url
