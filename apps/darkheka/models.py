from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


class Darkheka(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="Título")
    text = RichTextField()
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