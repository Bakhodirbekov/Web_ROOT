import uuid

from django.core import validators
from django.db import models

class Articles(models.Model):
    title = models.CharField('nomi', max_length=50)
    anons = models.CharField("Anons", max_length=250)
    full_text = models.TextField('Statya')
    date = models.DateTimeField('Qoyilgan vaqti')
    img = models.ImageField(upload_to='article_images/')  # Adjust 'article_images/' to your desired upload path

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'