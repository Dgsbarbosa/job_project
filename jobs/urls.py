from django.urls import path
from . import views

app_name = 'jobs'
urlpatterns = [
    path("index",views.index, name="index"),
    path("", views.about_us, name="about_us"),
    
    path("view_vacancy/<int:vacancy_id>",views.view_vacancy,name="view_vacancy"),    
    path("register_vacancy", views.register_vacancy, name='register_vacancy'),
    path("edit_vacancy/<int:vacancy_id>",views.edit_vacancy,name="edit_vacancy"),
    
    path("profiles/",views.profiles, name="profiles"),    
    path("edit_profile_candidate/<int:candidate_id>", views.edit_profile_candidate, name="edit_profile_candidate"),
    path("register_profile",views.register_profile,name="register_profile"),
    path("delete_company/<int:company_id>",views.delete_company,name="delete_company"),
    path("active_company/<int:company_id>", views.active_company, name="active_company"),
    
    path("register_company",views.register_company,name="register_company"),
    path("edit_company/<int:company_id>", views.edit_company, name="edit_company"),
    
    path("get_countries/",views.get_countries,name="get_countries"),
    path("get_states/<str:country_code>",views.get_states,name="get_states"),
    path("get_cities/<str:country_code>/<str:state_code>",views.get_cities,name="get_cities"),
    
    path("my_vacancies",views.my_vacancies,name="my_vacancies"),
    path("save_vacancy/<int:vacancy_id>", views.save_vacancy, name="save_vacancy"),
    path("saved_vacancies",views.saved_vacancies,name="saved_vacancies"),
    
    path("active_vacancy/<int:vacancy_id>", views.active_vacancy, name="active_vacancy")
    
    
]