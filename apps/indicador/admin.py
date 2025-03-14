from django.contrib import admin
from .models import NPS, FrontOfficeNPS,BackOfficeNPS,Interlocutores,HistoricoNPS

# Register your models here.
admin.site.register(NPS)
admin.site.register(FrontOfficeNPS)
admin.site.register(BackOfficeNPS)
admin.site.register(Interlocutores)
admin.site.register(HistoricoNPS)
