from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


class Darkheka(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="Título")
    text = CKEditor5Field('Text', config_name='extends')
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    keys = models.CharField(max_length=500,verbose_name="Chaves de pesquisa")
    image = models.ImageField(upload_to='images/darkheka', null=True, blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __str__(self):
        return self.title