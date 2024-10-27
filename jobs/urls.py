from django.urls import path
from . import views

app_name = 'jobs'
urlpatterns = [
    path("",views.index, name="index"),
    path("register_vacancy", views.register_vacancy, name='register_vacancy'),
    path("profiles/",views.profiles, name="profiles"),
    
    path("edit_profile_candidate/<int:candidate_id>", views.edit_profile_candidate, name="edit_profile_candidate"),
    path("register_profile",views.register_profile,name="register_profile"),
    path("register_company",views.register_company,name="register_company"),
    path("get_countries/",views.get_countries,name="get_countries"),
    path("get_states/<str:country_code>",views.get_states,name="get_states"),
    path("get_cities/<str:country_code>/<str:state_code>",views.get_cities,name="get_cities"),
    path("edit_company/<int:company_id>", views.edit_company, name="edit_company")
    
]