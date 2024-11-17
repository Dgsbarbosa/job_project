from .models import Vacancies, CompanyProfile, CandidateProfile
from django.forms import ModelForm, ModelChoiceField
from django import forms 

class VacanciesForm(ModelForm):
    
    class Meta:
        model = Vacancies
        exclude = ["id","created_at"]
        
        labels = {
            "company": "Nome da Empresa",
            "show_company": "Mostrar a empresa?"
        }
        widgets = {
            'contract_type':forms.Select(attrs={'class':""}),
            'phone1': forms.TextInput(attrs={"class":"phone","placeholder":"(33) 3333-3333","id":"phone1","hidden":True}),
            'phone2': forms.TextInput(attrs={"class":"phone","placeholder":"(99)9 9999-9999","id":"phone2",'hidden':True}),
            'email': forms.TextInput(attrs={"placeholder":"exemplo@exemplo.com","required":True}),
            'show_company': forms.CheckboxInput(attrs={"label":"Mostrar a empresa?"})
            
        }
        error_messages = {
            "city":{
                'required':'Por favor, informe a cidade.'
            },
            'state':{
                'required':'Por favor, informe o estado.'
            }
        }
  

class CandidateProfileForm(ModelForm):
    class Meta:
        model = CandidateProfile
        exclude = ["id","user","city","state","country","created_at"]
        widgets = {
            'phone1': forms.TextInput(attrs={"class":"phone","placeholder":"(33) 3333-3333","id":"phone1","hidden":True}),
            'phone2': forms.TextInput(attrs={"class":"phone","placeholder":"(99)9 9999-9999","id":"phone2",'hidden':True}),
            'email': forms.TextInput(attrs={"placeholder":"exemplo@exemplo.com","required":True}),
            
        }
        
class CompanyProfileForm(ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ["id","user","city","state","country","created_at"]
        
        