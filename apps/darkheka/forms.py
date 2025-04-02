from django import forms
from .models import Darkheka
from django_ckeditor_5.widgets import CKEditor5Widget



class DarkHekaForm(forms.ModelForm):
    class Meta:
        model = Darkheka
        fields = ['title', 'text', 'keys']

    widgets = {
        'title': forms.TextInput(attrs={'class':'form-control','placeholder': 'Título'}),
        'text': CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="comment"
              ),
        'keys': forms.Textarea(attrs={'class':'form-control','placeholder': 'Chaves'}),
    }