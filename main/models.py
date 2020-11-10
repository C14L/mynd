import hashlib

from django.db import models

from main.ndparsers import ndutils


class PageUrl(models.Model):
    url = models.URLField(null=False, blank=False)
    title = models.CharField(max_length=500, default="")
    author = models.CharField(max_length=500, default="")
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

    @property
    def count_different_texts(self):
        return len(set(self.texts.all().values_list("text_hashed", flat=True)))

    def save(self, *args, **kwargs):
        self.title = self.url
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.url


class PageText(models.Model):
    url = models.ForeignKey(PageUrl, on_delete=models.CASCADE, related_name="texts")
    created_on = models.DateTimeField(auto_now_add=True)

    _html = models.TextField(default="")
    html_hashed = models.CharField(max_length=32, default="")
    is_html_changed = models.BooleanField(default=True)

    _text = models.TextField(default="")
    text_hashed = models.CharField(max_length=32, default="")
    is_text_changed = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_on"]

    @property
    def html(self):
        return self._html

    @html.setter
    def html(self, value):
        self._html = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    def save(self, *args, **kwargs):
        self.html_hashed = ndutils.get_hash(self.html)
        self.text_hashed = ndutils.get_hash(self.text)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.url.url
