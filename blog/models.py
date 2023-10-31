from django.db import models

from mailing.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='Изображение')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    view_counts = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
