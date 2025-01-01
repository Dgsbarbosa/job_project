from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render,get_list_or_404, get_object_or_404
from .forms import VacanciesForm, CandidateProfileForm, CompanyProfileForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST,require_http_methods
from .models import CompanyProfile, CandidateProfile, Vacancies, SaveVacancy
import requests
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from collections import OrderedDict, defaultdict
from .utils import load_cache, save_cache, is_cache_expired, fetch_data_from_api

from user.models import CustomUser
import os


# Create your views here.

def get_countries(request):
    """Obtém a lista de países do cache ou da API."""
    if is_cache_expired():
        # Atualizar cache
        data = fetch_data_from_api("https://api.countrystatecity.in/v1/countries")
        if data:
            save_cache({"countries": data})
        else:
            data = load_cache().get("countries", [])
            
    else:
        # Carregar do cache
        data = load_cache().get("countries", [])
    
    return JsonResponse(data, safe=False)

def get_states(request, country_code):
    """Obtém a lista de estados para um país do cache ou da API."""
    cache = load_cache()
    if not cache or is_cache_expired() or "states" not in cache.get(country_code, {}):
        url = f"https://api.countrystatecity.in/v1/countries/{country_code}/states"
        states = fetch_data_from_api(url)
        
        if states:
            cache = cache or {}
            cache[country_code] = {"states": states}
            save_cache(cache)
        else:
            try:
                states = cache[country_code]["states"]
            except:
                 return JsonResponse({'error': 'Dont states'}, status=500)
    else:
        states = cache[country_code]["states"]
    
    return JsonResponse(states, safe=False)

def get_cities(request, country_code, state_code):
  
    cache = load_cache()
    key = f"{country_code}_{state_code}"
    
   
    if not cache or is_cache_expired() or "cities" not in cache.get(key, {}):
        url = f"https://api.countrystatecity.in/v1/countries/{country_code}/states/{state_code}/cities"
        cities = fetch_data_from_api(url)
        
        if cities:
            
          
            cache = cache or {}
            cache[key] = {"cities": cities}
            save_cache(cache)
        else:
            try:
                cities = cache[key]["cities"]
            except:
                 return JsonResponse({'error': 'API request failed'}, status=500)
    else:
        cities = cache[key]["cities"]
       
    return JsonResponse(cities, safe=False)

def index(request):

    
    vacancies_grouped_by_date = defaultdict(list)

    return_search = ""
    button_view_vacancies = False
    
    if request.method == "POST":

        filters = {}
        country = request.POST.get("country", "")
        state = request.POST.get("state", "")
        city = request.POST.get("city", "")
        position = request.POST.get("position", "")
        contract_type = request.POST.get("contract-type", "")

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
            
            return_search = {}
            # return_search = 
            for key in filters.keys():
                
                if key == "country":
                    key = "País"
                    return_search[key] = filters["country"]
                    
                elif key == "state":
                    key = "estado"
                    return_search[key] = filters["state"]

                elif key == "city":
                    key = "cidade"
                    return_search[key] = filters["city"]

                elif key == "title__icontains":
                    key = "cargo"
                    return_search[key] = filters["title__icontains"]

                elif key == "contract_type":
                    key = "tipo de contrato"
                    return_search[key] = filters["contract_type"]


            for chave, valor in return_search.items():

                if ":" in valor:
                    return_search[chave] = valor.split(":")[1]

        button_view_vacancies = True
        
        
    else:

        for vacancy in Vacancies.objects.all():
            date = vacancy.created_at.date()

            vacancies_grouped_by_date[date].append(vacancy)

    for date, vacancies in vacancies_grouped_by_date.items():

        vacancies.sort(key=lambda v: v.created_at, reverse=True)
        for vacancy in vacancies:
            country = vacancy.country
            country = country.split(":")[1]
            vacancy.country = country

            state = vacancy.state
            state = state.split(":")[1]
            vacancy.state = state

    vacancies_grouped_by_date = OrderedDict(
        sorted(vacancies_grouped_by_date.items(), reverse=True))

    vacancies_count = sum(len(v) for v in vacancies_grouped_by_date.values())
    context = {
        "vacancies_grouped_by_date": vacancies_grouped_by_date,
        "return_search": return_search,
        "button_view_vacancies": button_view_vacancies,
        "vacancies_count": vacancies_count

    }
    return render(request, "jobs/index.html", context)


def view_vacancy(request, vacancy_id):

    vacancy = Vacancies.objects.get(pk=vacancy_id)
    try:
        saved_vacancy = SaveVacancy.objects.filter(user=request.user, vacancy=vacancy.id)
    except:
        saved_vacancy = None
        
    country = vacancy.country
    country = country.split(":")[1]
    vacancy.country = country
    state = vacancy.state
    state = state.split(":")[1]
    vacancy.state = state

    
    context = {
        "vacancy": vacancy,
        "saved_vacancy":saved_vacancy
    }
    return render(request, "jobs/view_vacancy.html", context)

def about_us(request):
    
    return render(request, "jobs/about_us.html")

@login_required(login_url="auth/register")
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

                messages.success(request, "Perfil de Trabalhador salvo com sucesso.")

                return redirect("jobs:profiles")
            except:
                messages.error(
                    request, "Não foi possivel salvar o perfil. Tente novamente.")

    form = CandidateProfileForm()

    context = {
        "form": form
    }
    return render(request, "jobs/register_profile.html", context)


@login_required(login_url="auth/register")
def register_company(request):

    companies = CompanyProfile.objects.filter(user=request.user,is_active=True,is_deleted=False)

    if companies:
        messages.error(request,"No momento só é possivel o cadastro de uma empresa.")
        messages.error(request,"Aguarde as novas atualizações.")
        
        return redirect("jobs:profiles")
    
    
    if request.method == "POST":

        form = CompanyProfileForm(request.POST)

        if form.is_valid():

            try:
                company_profile = form.save(commit=False)
                company_profile.user = request.user
                company_profile.country = request.POST['country']
                company_profile.state = request.POST['state']
                company_profile.city = request.POST['city']
                company_profile.is_active = True

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
    companies_active = CompanyProfile.objects.filter(user=request.user,is_active=True, is_deleted=False).order_by("-is_active")
    companies_deactive = CompanyProfile.objects.filter(user=request.user,is_active=False, is_deleted=False).order_by("-is_active")
    if request.method == 'POST':
        form = VacanciesForm(request.POST)

        if form.is_valid():
            
            try:
                vacancy = form.save(commit=False)
                vacancy.company_id = request.POST['company']
                vacancy.country = request.POST['country']
                vacancy.state = request.POST['state']
                vacancy.city = request.POST['city']
                vacancy.is_active = True
                if vacancy.phone1 and len(vacancy.phone1) < 10:
                    vacancy.phone1 = ""
                if vacancy.phone2 and len(vacancy.phone2) < 10:
                    vacancy.phone2 = ""

                vacancy.save()
                
                

                messages.success(request, "Vaga cadastrada com suceso.")

                return redirect("jobs:index")
            except Exception as err:
                print("Error:", err)
                messages.error(
                    request, "Não foi possivel cadastrar a vaga. Tente novemente")
                
        else:
           errors = form.errors

           if errors:
            for field, error_list in errors.items():
                for error in error_list:
                    print(f"Erro no campo {field}: {error}")
                    messages.error(request,f"Erro no campo {field}: {error}")
                        
    else:
        companies_active = CompanyProfile.objects.filter(user=request.user,is_active=True, is_deleted=False).order_by("-is_active")
        companies_deactive = CompanyProfile.objects.filter(user=request.user,is_active=False, is_deleted=False).order_by("-is_active")
        form = VacanciesForm()

    context = {
        "companies_active": companies_active,
        "companies_deactive":companies_deactive,
        'form': form
    }
    return render(request, "jobs/register_vacancy.html", context)


@login_required(login_url="auth/register")
def edit_vacancy(request, vacancy_id):
    vacancy = Vacancies.objects.get(pk=vacancy_id)
    if request.method == "POST":
        
        form = VacanciesForm(request.POST, instance=vacancy)
        is_active = vacancy.is_active 

        if form.is_valid():
            
            vacancy_form = form.save(commit=False)

            vacancy_form.is_active = is_active
            vacancy_form.save()

            messages.success(request,"Vaga editada com sucesso")

        else:
            messages.error(request,f"Error: Não foi possível editar. Tente novamente. ")
            
        return redirect("jobs:view_vacancy", vacancy_id)

    else:        
        
        form = VacanciesForm(instance=vacancy)
        
        vacancy_country_name = vacancy.country
        vacancy_country_name = vacancy_country_name.split(":")[1]
        vacancy_state_name = vacancy.state
        vacancy_state_name = vacancy_state_name.split(":")[1]
        
        if form["phone1"].value():
            form.fields["phone1"].widget.attrs['hidden'] = False
            
        if form["phone2"].value():
            form.fields["phone2"].widget.attrs['hidden'] = False

      
        
        context = {
            "form": form,
            "vacancy": vacancy,
            "vacancy_country_name": vacancy_country_name,
            "vacancy_state_name": vacancy_state_name
        }
        return render(request, "jobs/edit_vacancy.html", context)


@login_required(login_url="auth/register")
def profiles(request):

    company_profile = ""
    company_profile_inactive = ""

    try:
        candidate_profile = CandidateProfile.objects.get(user=request.user)
        
        country = candidate_profile.country
        state = candidate_profile.state
        
        country = country.split(":")[1]
        candidate_profile.country = country
        state = state.split(":")[1]
        candidate_profile.state = state

    except CandidateProfile.DoesNotExist:
        messages.warning(request, "Cadastre um Perfil do Candidato")
        candidate_profile = None
    except:
        messages.error(
            request, f"Não foi possivel carregar o Perfil do Candidato")

    try:
        count_company_profile = CompanyProfile.objects.filter(user=request.user, is_deleted=False).count()

        if count_company_profile > 1:
            company_profile = CompanyProfile.objects.filter(user=request.user, is_active=True,is_deleted=False)
            company_profile_inactive = CompanyProfile.objects.filter(user=request.user, is_active=False,is_deleted=False)
            for company in company_profile:
                
                country = company.country
                state = company.state
                
                country = country.split(":")[1]
                company.country = country
                state = state.split(":")[1]
                company.state = state
                
            for company in company_profile_inactive:
                
                country = company.country
                state = company.state
                
                country = country.split(":")[1]
                company.country = country
                state = state.split(":")[1]
                company.state = state

        elif count_company_profile == 1:
            company_profile = CompanyProfile.objects.get(user=request.user,is_deleted=False)
                 
            country = company_profile.country
            state = company_profile.state
            
            country = country.split(":")[1]
            company_profile.country = country
            state = state.split(":")[1]
            company_profile.state = state
        
   
        
    except Exception as error:
        company_profile = None
        print(error)
        messages.error(request, "Não foi possivel carregar os Perfis de Empresas.")
    
    print(company_profile, count_company_profile)
    
    if count_company_profile == 0:
        messages.warning(request, "Cadastre um Perfil de Empresa")
    elif count_company_profile > 1:
        
        count_company_profile_inactive = 0
        
        for company in company_profile:
            if company.is_active == False:
                count_company_profile_inactive += 1
                
        if count_company_profile - company_profile_inactive.count() == 0:
            
            print("todas desativadas")
            messages.warning(request, "Cadastre ou reative o Perfil de Empresa")     
    

    context = {
        'candidate_profile': candidate_profile,
        'company_profile': company_profile,
        'company_profile_inactive':company_profile_inactive,
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
        
        phone1_value = form['phone1'].value()
        if phone1_value and len(phone1_value) < 7:  # Garantir que phone1 não é None
            # Atualizar o valor do campo no dicionário POST
            request.POST = request.POST.copy()  # Tornar mutável
            request.POST['phone1'] = ""
        phone2_value = form['phone2'].value()
        if phone2_value and len(phone2_value) < 7:  # Garantir que phone1 não é None
            # Atualizar o valor do campo no dicionário POST
            request.POST = request.POST.copy()  # Tornar mutável
            request.POST['phone2'] = ""   

        if form.is_valid():

            try:
                candidate_profile = form.save(commit=False)

                candidate_profile.country = request.POST['country']
                candidate_profile.state = request.POST['state']
                candidate_profile.city = request.POST['city']

                candidate_profile.save()
                messages.success(request, "O Perfil de Trabalhador foi alterado com sucesso")

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
    company_active = company.is_active
    

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
                 
        resume_company = request.POST['resume_company'] 
        resume_company = resume_company.strip() 
        
                
        if form.is_valid():
            try:
                
                company_profile = form.save(commit=False)
                company_profile.country = request.POST['country']
                company_profile.state = request.POST['state']
                company_profile.city = request.POST['city']
                company_profile.is_active = company_active
                
                

                company_profile.save()
                messages.success(request, f"Empresa atualizada com sucesso")

                return redirect("jobs:profiles")
            except Exception as err:
                messages.error(
                    request, f"Não foi possivel atualizar a empresa. Tente novamente ")
        else:
            messages.error(request,"Erro no formulario")
            print(form.errors)
    
    form = CompanyProfileForm(instance=company)

    context = {
        "form": form,
        "company": company,
        "company_country_split": company_country_split,
        "company_state_split": company_state_split
    }
    return render(request, "jobs/edit_company.html", context)

@login_required(login_url="auth/register")
def my_vacancies(request):
    
    companies = CompanyProfile.objects.filter(user_id=request.user).all()

    vacancies_grouped_by_company_active = defaultdict(list)
    
    for company in companies:
        for vacancy in Vacancies.objects.filter(company_id=company.id,is_active=True):
                
                company_name = company.company_name
                vacancies_grouped_by_company_active[company_name].append(vacancy)

    for date, vacancies in vacancies_grouped_by_company_active.items():

        vacancies.sort(key=lambda v: v.created_at, reverse=True)
        for vacancy in vacancies:
            country = vacancy.country
            country = country.split(":")[1]
            vacancy.country = country

            state = vacancy.state
            state = state.split(":")[1]
            vacancy.state = state

    vacancies_grouped_by_company_active = OrderedDict(
        sorted(vacancies_grouped_by_company_active.items(), reverse=True))

    vacancies_count = sum(len(v) for v in vacancies_grouped_by_company_active.values())
    
    vacancies_grouped_by_company_disable = defaultdict(list)
    
    for company in companies:
        for vacancy in Vacancies.objects.filter(company_id=company.id,is_active=False):
                
                company_name = company.company_name
                vacancies_grouped_by_company_disable[company_name].append(vacancy)

    for date, vacancies in vacancies_grouped_by_company_disable.items():

        vacancies.sort(key=lambda v: v.created_at, reverse=True)
        for vacancy in vacancies:
            country = vacancy.country
            country = country.split(":")[1]
            vacancy.country = country

            state = vacancy.state
            state = state.split(":")[1]
            vacancy.state = state

    vacancies_grouped_by_company_disable = OrderedDict(
        sorted(vacancies_grouped_by_company_disable.items(), reverse=True))

    vacancies_count_active = sum(len(v) for v in vacancies_grouped_by_company_active.values())
    vacancies_count_deactive = sum(len(v) for v in vacancies_grouped_by_company_disable.values())
    
    vacancies_count = vacancies_count_active + vacancies_count_deactive
    context = {
        "vacancies_grouped_by_company_active": vacancies_grouped_by_company_active, 
        "vacancies_grouped_by_company_disable":vacancies_grouped_by_company_disable,      
        "vacancies_count": vacancies_count
    }
    
    return render(request,"jobs/my_vacancies.html", context)


@login_required(login_url="/auth/register")
@require_POST
def save_vacancy(request, vacancy_id):
    
    try:
        vacancy = get_object_or_404(Vacancies, id=vacancy_id)

        saved_vacancy, created = SaveVacancy.objects.get_or_create(user=request.user, vacancy=vacancy)
        
        if created:
            status = "saved"
            
            
        else:
            saved_vacancy.delete()
            status = "unsaved"
            
            
        return  JsonResponse({'status':status})
    except:
        pass
    
@login_required(login_url="auth/register")
def saved_vacancies(request):
    try:
        saved_vacancies = SaveVacancy.objects.filter(user=request.user).select_related("vacancy").order_by("-saved_at")
        vacancies_count = saved_vacancies.count()
        
        for saved in saved_vacancies:
            country = saved.vacancy.country
            country = country.split(":")[1]
            saved.vacancy.country = country
            state = saved.vacancy.state
            state = state.split(":")[1]
            saved.vacancy.state = state
        
        context = {
            "saved_vacancies":saved_vacancies,
            "vacancies_count":vacancies_count,
        
        }
        return render(request,"jobs/saved_vacancies.html",context)
    except:
        pass

@login_required(login_url="auth/register")
def active_vacancy(request, vacancy_id):
    
    vacancy = Vacancies.objects.get(id=vacancy_id)
    
    
    try:
        if vacancy.is_active:
            vacancy.is_active = False

        else:
            vacancy.is_active = True
        
        vacancy.save()
        messages.success(request, "Alterado com sucesso")
        message = {"message":"success"}
    except:
        
        messages.error(request,"Não foi possivel alterar a vaga. Tente novamente")
        message = {"message":"error"}

    return JsonResponse(message)


@login_required(login_url="auth/register")
def delete_company(request,company_id):
    
    try:
        company = CompanyProfile.objects.get(id=company_id)
        
        if company.vacancies.exists():
            for vancancy in company.vacancies.all():
                vancancy.is_active = False
                vancancy.save()
                
        company.is_deleted = True
        company.is_active = False
        company.save()
        
        messages.success(request,"Empresa deletada com sucesso.")
        message = "success"
    except:
        messages.error(request,"Não foi possivel deletar a empresa.")
        message = "Error: não foi possivel deletar a empresa. Tente novamente."
        
    return JsonResponse({"message":message},status=200)


@login_required(login_url="auth/register")
def active_company(request,company_id):
   
    
    company = CompanyProfile.objects.get(id=company_id)
    
    if company.is_active:
        company.is_active = False
        for vancancy in company.vacancies.all():
            vancancy.is_active = False
            vancancy.save()
        
    else:
        
        companies_active_count = CompanyProfile.objects.filter(user=request.user,is_active=True).count()
        
        if companies_active_count < 1:
            company.is_active = True
            
        else:
            messages.error(request,"No momento só é possivel uma empresa ativa por vez.")
            messages.error(request,"Aguarde atualizações.")
            
    company.save()
    
    
    return redirect("jobs:profiles")
    







