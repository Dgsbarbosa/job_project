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

        def __init__(self,*args, **kwargs):
            
            super(VacanciesForm,self).__init__(*args,**kwargs)
            print(self.user)
            if hasattr(self,'user'):
                
                self.fields['company'].queryset = CompanyProfile.objects.filter(user_id=self.user.id)

class CandidateProfileForm(ModelForm):
    class Meta:
        model = CandidateProfile
        exclude = ["id","user","city","state","country","created_at"]
        
class CompanyProfileForm(ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ["id","user","city","state","country","created_at"]