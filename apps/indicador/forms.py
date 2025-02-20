from django import forms
from .models import ExcelFile

class NpsFileUploadForm(forms.ModelForm):
    class Meta:
        model = ExcelFile
        fields = ['arquivo']

    widgets = {
        'arquivo': forms.FileInput(attrs={'class':'form-control','placeholder': 'NPS mensal'})
    }
    
    def clean_arquivo(self):
        arquivo = self.cleaned_data["arquivo"]  # Aqui está a correção, sem o "_get"
        if not arquivo.name.endswith('.xlsx') and not arquivo.name.endswith('.xls'):
            raise forms.ValidationError('Apenas ficheiros Excel (.xlsx, .xls) são permitidos')
        return arquivo
    

class RechamadaUploadForm(forms.ModelForm):
    class Meta:
        model = ExcelFile
        fields = ['arquivo']

    widgets = {
        'arquivo': forms.FileInput(attrs={'class':'form-control','placeholder': 'Rechamada'})
    }
    
    def clean_arquivo(self):
        arquivo = self.cleaned_data_get("arquivo")
        if not arquivo.name.endswith('.xlsx','.xls'):
            raise forms.ValidationError('Apenas ficheiros Excel (.xlsx, .xls) sao permitidos')
        return arquivo

class ProvisoriosUploadForm(forms.ModelForm):
    class Meta:
        model = ExcelFile
        fields = ['arquivo']
    
    widgets = {
        'arquivo': forms.FileInput(attrs={'class':'form-control','placeholder': 'Provisorios'})
    }
    
    def clean_arquivo(self):
        arquivo = self.cleaned_data_get("arquivo")
        if not arquivo.name.endswith('.xlsx','.xls'):
            raise forms.ValidationError('Apenas ficheiros Excel (.xlsx, .xls) sao permitidos')
        return arquivo