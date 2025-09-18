from apps.iqs.models import TipoIqs
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def criar_tipos_iqs(sender, **kwargs):
    name = ['Transferida FO', 'Transferida BO', 'Não transferida FO', 'Não transferida BO']
    if not TipoIqs.objects.filter(name='Transferida FO').exists():
        for n in name:
            TipoIqs.objects.create(name=n)
    
    
            