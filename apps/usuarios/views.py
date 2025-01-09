from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        """Chamado quando o formulário é válido (credenciais corretas)."""
        user = form.get_user()
        login(self.request, user)

        # Lógica de redirecionamento baseada no tipo de usuário
        if hasattr(user, 'usuario') and user.usuario.tipo.tipo == "Supervisor":
            return redirect('home')
        elif hasattr(user, 'usuario') and user.usuario.tipo.tipo == "Assistente":
            return redirect('lista_intervalos')
        else:
            messages.error(self.request, "Tipo de usuário desconhecido.")
            return redirect('login')

    def form_invalid(self, form):
        """Chamado quando o formulário é inválido (credenciais incorretas ou campos vazios)."""
        # Logs para verificar quando o método é chamado
        print("Chamando form_invalid")

        # Obter o username do formulário
        username = self.request.POST.get('username', '')
        if not username:
            messages.error(self.request, "O campo de nome de usuário está vazio.")
        elif not self.request.POST.get('password'):
            messages.error(self.request, "O campo de palavra-passe está vazio.")
        elif not User.objects.filter(username=username).exists():
            messages.error(self.request, "O nome de usuário não existe.")
        else:
            messages.error(self.request, "A palavra-passe está incorreta.")

        # Renderiza novamente a página com o formulário inválido e as mensagens
        return self.render_to_response(self.get_context_data(form=form))


"""def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username= form.cleaned_data.get('username')
            password= form.cleaned_data.get('password')

            if not User.objects.filter(username=username).exists():
                messages.error(request, 'O nome de usuário não existe.')
            else:
                user = authenticate(request,username=username,
                                    password=password)
                if user is not None:
                    login(request, user)
                    if user.usuario.tipo.tipo == "Supervisor":
                        redirect('home')
                    elif user.usuario.tipo.tipo == "Assistente":
                        redirect('lista_intervalos')
                else:
                    messages.error(request,"A palavra pass está incorreta!")

        else:
            messages.error(request, "Erro no formulário")
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})"""