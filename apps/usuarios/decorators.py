from django.http import HttpResponseForbidden
from .models import Usuario

def user_is_assistente(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            # Acesse o objeto Usuario através do usuário autenticado (request.user)
            usuario = request.user.usuario
            if usuario.tipo.tipo != 'Assistente':
                return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
        except Usuario.DoesNotExist:
            return HttpResponseForbidden("Usuário não encontrado.")
        
        # Se o tipo do usuário for 'Assistente', continue com a view
        return view_func(request, *args, **kwargs)

    return _wrapped_view