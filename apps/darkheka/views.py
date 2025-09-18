import os

from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Darkheka
from .forms import DarkHekaForm




class DarkHekaList(ListView):
    model = Darkheka
    template_name = 'darkheka/darkheka_list.html'
    context_object_name = 'heka_list'

    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['darkheka/darkheka_list_partial.html']
        return ['darkheka/darkheka_list.html']

    


class CreateDarkHeka(CreateView):
    model = Darkheka
    model_form_class = DarkHekaForm
    success_url = '/darkheka/darkhekamain'
    fields = ['title', 'text', 'keys']

    def get_context_data(self, **kwargs):
        context = super(CreateDarkHeka, self).get_context_data(**kwargs)
        context['heka_list'] = Darkheka.objects.all()
        return context
    
    def form_valid(self, form):
        form.save()
        return super(CreateDarkHeka, self).form_valid(form) 
    
    def form_invalid(self, form):
        return super(CreateDarkHeka, self).form_invalid(form)
    
    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['darkheka/darkheka_form_partial.html']
        return ['darkheka/darkheka_form.html']
    

class DarkhekaDetail(DetailView):
    model = Darkheka
    template_name = 'darkheka/darkheka_detail.html'
    context_object_name = 'darkheka'

    def get_context_data(self, **kwargs):
        context = super(DarkhekaDetail, self).get_context_data(**kwargs)
        context['heka_list'] = Darkheka.objects.all()
        return context
    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['darkheka/darkheka_detail_partial.html']
        return ['darkheka/darkheka_detail.html']

class DarkhekaUpdate(UpdateView):
    model = Darkheka
    fields = ['title', 'text', 'keys']
    template_name = 'darkheka/darkheka_form.html'
    queryset = Darkheka.objects.all()
    success_url = '/darkheka/darkhekamain'

    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['darkheka/darkheka_form_partial.html']
        return ['darkheka/darkheka_form.html']






def delete_darkheka(request, pk):
    darkheka = Darkheka.objects.get(pk=pk)
    darkheka.delete()
    return render(request, 'darkheka/darkheka_list.html')

@csrf_exempt
def custom_upload_file(request):
    if request.method == "POST" and request.FILES.get("upload"):
        uploaded_file = request.FILES["upload"]
        upload_dir = "media/uploads"

        # Garante que o diretório existe
        os.makedirs(upload_dir, exist_ok=True)

        upload_path = os.path.join(upload_dir, uploaded_file.name)

        with open(upload_path, "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return JsonResponse({
            "url": f"/media/uploads/{uploaded_file.name}",
            "uploaded": True
        })

    return JsonResponse({"error": "Invalid request"}, status=400)