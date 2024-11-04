from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render,get_list_or_404, get_object_or_404
from .forms import VacanciesForm, CandidateProfileForm, CompanyProfileForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import CompanyProfile, CandidateProfile, Vacancies, SaveVacancy
import requests
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from collections import OrderedDict, defaultdict
from . import utils
from user.models import CustomUser


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
        companies = CompanyProfile.objects.filter(user=request.user)
        form = VacanciesForm()

    context = {
        "companies": companies,
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

    except CandidateProfile.DoesNotExist:
        messages.warning(request, "Cadastre um perfil")
        candidate_profile = None
    except:
        messages.error(
            request, f"Não foi possivel carregar o Perfil do Candidato")

    try:
        count_company_profile = CompanyProfile.objects.filter(
            user=request.user).count()

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
            company_profile = CompanyProfile.objects.get(user=request.user)
            
            country = company_profile.country
            state = company_profile.state
            
            country = country.split(":")[1]
            company_profile.country = country
            state = state.split(":")[1]
            company_profile.state = state
        
    except:
        company_profile = None
        messages.error(
            request, "Não foi possivel carregar os Perfis de Empresas")

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
                messages.success(request, f"Empresa atualizada com sucesso")

                return redirect("jobs:profiles")
            except Exception as err:
                messages.error(
                    request, f"Não foi possivel atualizar a empresa. Tente novamente ")

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

    vacancies_count = sum(len(v) for v in vacancies_grouped_by_company_disable.values())
    
    context = {
        "vacancies_grouped_by_company_active": vacancies_grouped_by_company_active, 
        "vacancies_grouped_by_company_disable":vacancies_grouped_by_company_disable,      
        "vacancies_count": vacancies_count
    }
    
    return render(request,"jobs/my_vacancies.html", context)


@login_required(login_url="auth/register")
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
        company.is_deleted = True

        company.save()
        
        messages.success(request,"Empresa deletada com sucesso.")
        message = "success"
    except:
        messages.error(request,"Não foi possivel deletar a empresa.")
        message = "error"
    return JsonResponse({"message":message})


@login_required(login_url="auth/register")
def active_company(request,company_id):
   
    
    company = CompanyProfile.objects.get(id=company_id)
    if company.is_active:
        company.is_active = False
    else:
        company.is_active = True
    
    company.save()
    
    return redirect("jobs:profiles")
    







