from . import views
from django.urls import path

app_name = "user"
urlpatterns = [
    path("register/",views.register,name="register"),
    path("edit_user",views.edit_user,name="edit_user"),
    
    path("login_view",views.login_view, name="login_view" ),
    path("logout_view", views.logout_view,name="logout_view")
    
]
