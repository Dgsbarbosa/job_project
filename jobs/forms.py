from .models import Vacancies, CompanyProfile, CandidateProfile
from django.forms import ModelForm, ModelChoiceField
from django import forms 

class VacanciesForm(ModelForm):
    
    class Meta:
        model = Vacancies
        exclude = ["id","created_at"]
        
        labels = {
            "company": "Nome da Empresa"
        }
        widgets = {
            'contract_type':forms.Select(attrs={'class':"form-select select-type-contract"}),
            'phone1': forms.TextInput(attrs={"class":"phone","placeholder":"3333-3333"}),
            'phone2': forms.TextInput(attrs={"class":"phone","placeholder":"9 9999-9999"})
            
        }
  

class CandidateProfileForm(ModelForm):
    class Meta:
        model = CandidateProfile
        exclude = ["id","user","city","state","country","created_at"]
        
class CompanyProfileForm(ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ["id","user","city","state","country","company_name","created_at"]