from django.contrib import admin
from .models import BackOffice,BackofficeConfig,BackOfficeDiario,BackOfficeFilaEspera

# Register your models here.
admin.site.register(BackOffice)
admin.site.register(BackofficeConfig)
admin.site.register(BackOfficeDiario)
admin.site.register(BackOfficeFilaEspera)