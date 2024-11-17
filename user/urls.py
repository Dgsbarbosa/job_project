from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = "user"
urlpatterns = [
    
    path("register/",views.register,name="register"),
    
    path("view_user",views.view_user, name="view_user"),
    path("edit_user",views.edit_user,name="edit_user"),
    
    path("login_view",views.login_view, name="login_view" ),
    path("logout_view", views.logout_view,name="logout_view"),
    
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
]
