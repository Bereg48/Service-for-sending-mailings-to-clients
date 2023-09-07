import uuid

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.text import slugify

NULLABLE = {'blank': True, 'null': True}


class Contacts(models.Model):
    contact_text = models.TextField(verbose_name='контакты', **NULLABLE)

    def __str__(self):
        return 'Контакты'


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(verbose_name='slug', max_length=255, unique=True)
    text = models.TextField(verbose_name='содержимое', **NULLABLE)
    image = models.ImageField(upload_to='blog_image/', verbose_name='изображение', **NULLABLE)
    date = models.DateField(verbose_name='дата создания', auto_now_add=True, **NULLABLE)
    view_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True, verbose_name='публикация')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            while Blog.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:6]}"
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ('view_count',)
