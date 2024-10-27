from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import VacanciesForm, CandidateProfileForm, CompanyProfileForm
from django.contrib.auth.decorators import login_required
from .models import CompanyProfile, CandidateProfile,Vacancies
import requests
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from collections import OrderedDict, defaultdict

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


def get_states(request, country_code):
    url = f"https://api.countrystatecity.in/v1/countries/{country_code}/states"

    headers = {
        'X-CSCAPI-KEY': settings.COUNTRYSTATECITY_API_KEY
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()

    return JsonResponse(data, safe=False)


def get_cities(request, country_code, state_code):
    url = f"https://api.countrystatecity.in/v1/countries/{country_code}/states/{state_code}/cities"

    headers = {
        'X-CSCAPI-KEY': settings.COUNTRYSTATECITY_API_KEY
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()

    return JsonResponse(data, safe=False)


def index(request):
    
    vacancies_grouped_by_date = defaultdict(list)
    
    return_search = ""
    button_view_vacancies = False
    if request.method == "POST":
        
        filters = {}
        country = request.POST.get("country","")
        state = request.POST.get("state","")
        city = request.POST.get("city","")
        position = request.POST.get("position","")
        contract_type = request.POST.get("contract-type","")
        
        if country:
            filters["country"] = country
        if state:
            filters["state"] = state
        if city:
            filters["city"] = city
        if position:
            filters["title__icontains"] = position
        if contract_type:
            filters["contract_type"] = contract_type
        
        
        for vacancy in Vacancies.objects.filter(**filters):
            date = vacancy.created_at.date()
            vacancies_grouped_by_date[date].append(vacancy)           
        
        if not vacancies_grouped_by_date.items():
            return_search = filters 
            
            for chave,valor in return_search.items():
                
                if ":" in valor:
                    return_search[chave] = valor.split(":")[1]
        
        button_view_vacancies = True
        
        
    else:
        
        for vacancy in Vacancies.objects.all():
            date = vacancy.created_at.date() 
            
            vacancies_grouped_by_date[date].append(vacancy)

    for date, vacancies in vacancies_grouped_by_date.items():
        
        vacancies.sort(key=lambda v: v.created_at,reverse=True)
        for vacancy in vacancies:
            country = vacancy.country  
            country = country.split(":")[1] 
            vacancy.country = country 
            
            state = vacancy.state 
            state = state.split(":")[1]
            vacancy.state = state
                
        
    vacancies_grouped_by_date = OrderedDict(sorted(vacancies_grouped_by_date.items(),reverse=True))
    
    vacancies_count = sum(len(v) for v in vacancies_grouped_by_date.values())
    context = {
        "vacancies_grouped_by_date":vacancies_grouped_by_date,
        "return_search":return_search,
        "button_view_vacancies":button_view_vacancies,
        "vacancies_count":vacancies_count

    }
    return render(request, "jobs/index.html", context)


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

                messages.success(request, "Perfil salvo com sucesso.")

                return redirect("jobs:profiles")
            except:
                messages.error(
                    request, "Não foi possivel salvar o perfil. Tente novamente.")

    form = CandidateProfileForm()

    context = {
        "form": form
    }
    return render(request, "jobs/register_profile.html", context)


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

                messages.success(request, "Empresa salva com suceso")

                return redirect("jobs:profiles")

            except:

                form = CompanyProfileForm(request.POST)
                messages.error(request, "Não foi possivel salvar a empresa")

    else:
        form = CompanyProfileForm()
    context = {
        "form": form
    }

    return render(request, "jobs/register_company.html", context)


@login_required(login_url="auth/register")
def register_vacancy(request):
    companies = CompanyProfile.objects.filter(user=request.user)
    if request.method == 'POST':
        form = VacanciesForm(request.POST)
        
        if form.is_valid():
            
            try:
                vacancy = form.save(commit=False)
                vacancy.company_id = request.POST['company']
                vacancy.country = request.POST['country']
                vacancy.state = request.POST['state']
                vacancy.city = request.POST['city']
                
                if len(vacancy.phone1) < 10:
                    vacancy.phone1 = ""
                if len(vacancy.phone2) < 10:
                    vacancy.phone2 = ""    
                
                vacancy.save()
                
                
                messages.success(request,"Vaga cadastrada com suceso.")

                return redirect("jobs:index")
            except:
                
                messages.error(request,"Não foi possivel cadastrar a vaga. Tente novemente")
    else:
        companies = CompanyProfile.objects.filter(user=request.user)
        form = VacanciesForm()
        

    context = {
        "companies":companies,
        'form': form
    }
    return render(request, "jobs/register_vacancy.html", context)


@login_required(login_url="auth/register")
def profiles(request):

    company_profile = ""

    try:
        candidate_profile = CandidateProfile.objects.get(user=request.user)

    except CandidateProfile.DoesNotExist:
        messages.warning(request,"Cadastre um perfil")
        candidate_profile = None
    except:
        messages.error(request, f"Não foi possivel carregar o Perfil do Candidato" )

    try:
        count_company_profile = CompanyProfile.objects.filter(
            user=request.user).count()

        if count_company_profile > 1:
            company_profile = CompanyProfile.objects.filter(user=request.user)

        elif count_company_profile == 1:
            company_profile = CompanyProfile.objects.get(user=request.user)

    except:
        company_profile = None
        messages.error(
            request, "Não foi possivel carregar os Perfis de Empresas")

    context = {
        'candidate_profile': candidate_profile,
        'company_profile': company_profile,
        'count_company_profile': count_company_profile
    }
    return render(request, "jobs/profiles.html", context)


@login_required(login_url="auth/register")
def edit_profile_candidate(request, candidate_id):

    candidate = CandidateProfile.objects.get(id=candidate_id)
    candidate_country_name = candidate.country.split(":")[1]
    candidate_state_name = candidate.state.split(":")[1]

    if request.method == "POST":
        form = CandidateProfileForm(request.POST, instance=candidate)

        if form.is_valid():

            try:
                candidate_profile = form.save(commit=False)

                candidate_profile.country = request.POST['country']
                candidate_profile.state = request.POST['state']
                candidate_profile.city = request.POST['city']

                candidate_profile.save()
                messages.success(request, "O perfil foi alterado com sucesso")

                return redirect("jobs:profiles")

            except:
                messages.error(
                    request, "Não foi possivel alterar o perfil. Tente novamente.")
                pass
        else:
            messages.error(request, " Formulario Inválido. Tente novamente.")

    form = CandidateProfileForm(instance=candidate)

    context = {
        "form": form,
        "candidate": candidate,
        "candidate_country_name": candidate_country_name,
        "candidate_state_name": candidate_state_name
    }
    return render(request, "jobs/edit_profile_candidate.html", context)


@login_required(login_url="auth/register")
def edit_company(request, company_id):

    company = CompanyProfile.objects.get(pk=company_id)
    
    try:
        company_country_split = company.country.split(":")[1]
    except:
        company_country_split = company.country
    try:
        company_state_split = company.state.split(":")[1]
    except:
        company_state_split = company.state
        
    if request.method == "POST":

        form = CompanyProfileForm(request.POST, instance=company)

        if form.is_valid():
            try:
                company_profile = form.save(commit=False)
                company_profile.country = request.POST['country']
                company_profile.state = request.POST['state']
                company_profile.city = request.POST['city']

                company_profile.save()
                messages.success(request,f"Empresa atualizada com sucesso")
                
                return redirect("jobs:profiles")
            except Exception as err:
                messages.error(request,f"Não foi possivel atualizar a empresa. Tente novamente ")
                
    form = CompanyProfileForm(instance=company)

    context = {
        "form": form,
        "company": company,
        "company_country_split": company_country_split,
        "company_state_split":company_state_split
    }
    return render(request, "jobs/edit_company.html", context)
