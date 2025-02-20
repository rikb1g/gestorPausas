from django.contrib import admin
from .models import NPS, FrontOfficeNPS,BackOfficeNPS

# Register your models here.
admin.site.register(NPS)
admin.site.register(FrontOfficeNPS)
admin.site.register(BackOfficeNPS)
