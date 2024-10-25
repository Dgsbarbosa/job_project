from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import VacanciesForm, CandidateProfileForm, CompanyProfileForm
from django.contrib.auth.decorators import login_required
from .models import CompanyProfile, CandidateProfile
import requests
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
# Create your views here.

def get_countries(request):
    
    url = "https://api.countrystatecity.in/v1/countries"

    headers = {
    'X-CSCAPI-KEY': settings.COUNTRYSTATECITY_API_KEY
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'API request failed'}, status=500)
    
   
def get_states(request,country_code):
    url = f"https://api.countrystatecity.in/v1/countries/{country_code}/states"

    headers = {
    'X-CSCAPI-KEY': settings.COUNTRYSTATECITY_API_KEY
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()
    
    
    return JsonResponse(data,safe=False)

def get_cities(request,country_code,state_code):
    url = f"https://api.countrystatecity.in/v1/countries/{country_code}/states/{state_code}/cities"

    headers = {
    'X-CSCAPI-KEY': settings.COUNTRYSTATECITY_API_KEY
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()
    
    return JsonResponse(data,safe=False)


def index(request):
    
    
   
    return render(request,"jobs/index.html")


def register_profile(request):
        
    if request.method == "POST":
        
        form = CandidateProfileForm(request.POST)    
        
        if form.is_valid():
            
            try:
                candidate_profile = form.save(commit=False)
                candidate_profile.user = request.user
                
                candidate_profile.country = request.POST['country']
                candidate_profile.state = request.POST['state']
                candidate_profile.city = request.POST['city']
                candidate_profile.personal_sumary = request.POST['personal_sumary']
                candidate_profile.professional_sumary = request.POST['professional_sumary']

                candidate_profile.save()

                messages.success(request,"Perfil salvo com sucesso.")
                
                return redirect("jobs:profiles")
            except :
                messages.error(request,"Não foi possivel salvar o perfil. Tente novamente.")

             
    form = CandidateProfileForm()

    context = {
        "form":form
    }
    return render(request,"jobs/register_profile.html", context)


def register_company(request):
    
    
    if request.method == "POST":
        
        form = CompanyProfileForm(request.POST)
        
        if form.is_valid():
            
            try:
                company_profile = form.save(commit=False)
                company_profile.user = request.user
                company_profile.country = request.POST['country']
                company_profile.state = request.POST['state']
                company_profile.city = request.POST['city']
                
                company_profile.save()
                
                messages.success(request,"Empresa salva com suceso")
                
                return redirect("jobs:profiles")

            except:     

                form = CompanyProfileForm(request.POST)
                messages.error(request,"Não foi possivel salvar a empresa")
                
    else:
        form = CompanyProfileForm()
    context = {
        "form":form
    }
    
    return render (request,"jobs/register_company.html", context)

@login_required(login_url="auth/register")
def register_vacancy(request):
    
    form = VacanciesForm()
    form.user = request.user
    
    
    
    context = {
        'form':form
    }
    return render(request,"jobs/register_vacancy.html", context)

@login_required(login_url="auth/register")
def profiles(request):
    
    company_profile = ""
    
    try:
        
        candidate_profile = CandidateProfile.objects.get(user = request.user)
    except:
        candidate_profile=None
        messages.error(request, "Não foi possivel carregar o Perfil do Candidato")
        
    try:    
        count_company_profile = CompanyProfile.objects.filter(user = request.user).count()
   
         
        
        if count_company_profile > 1:
            company_profile = CompanyProfile.objects.filter(user = request.user)
            
        elif count_company_profile == 1:
            company_profile = CompanyProfile.objects.get(user=request.user)              
                
    except:
        company_profile =None
        messages.error(request, "Não foi possivel carregar os Perfis de Empresas")
    
    context = {
        'candidate_profile':candidate_profile,
        'company_profile':company_profile,
        'count_company_profile':count_company_profile
    }
    return render(request, "jobs/profiles.html",context)


@login_required(login_url="auth/register")
def edit_profile_candidate(request, candidate_id):   
    
    candidate = CandidateProfile.objects.get(id=candidate_id)
    candidate_country_name = candidate.country.split(":")[1]
    candidate_state_name = candidate.state.split(":")[1]
    
    
    if request.method == "POST":
        form = CandidateProfileForm(request.POST,instance=candidate)
        
        if form.is_valid():
            
            try:
                candidate_profile = form.save(commit=False)
                
                candidate_profile.country = request.POST['country']
                candidate_profile.state = request.POST['state']
                candidate_profile.city = request.POST['city']

                candidate_profile.save()
                messages.success(request,"O perfil foi alterado com sucesso")

                return redirect("jobs:profiles")
            
            except:
                messages.error(request,"Não foi possivel alterar o perfil. Tente novamente.")
                pass
            
    form = CandidateProfileForm(instance=candidate)
    
    
    context = {
        "form":form,
        "candidate":candidate,
        "candidate_country_name":candidate_country_name,
        "candidate_state_name":candidate_state_name
    }
    return render(request,"jobs/edit_profile_candidate.html", context)