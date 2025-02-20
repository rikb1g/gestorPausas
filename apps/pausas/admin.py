from django.contrib import admin
from .models import Pausa, ConfiguracaoPausa, FilaEspera, PausasDiarias,ConfiguracaoPausa2
# Register your models here.

admin.site.register(Pausa)
admin.site.register(ConfiguracaoPausa)
admin.site.register(FilaEspera)
admin.site.register(PausasDiarias)
admin.site.register(ConfiguracaoPausa2)