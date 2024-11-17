from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import CustomUser
from.form import CustomUserForm
from . import utils
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def register(request):
    
    if request.method == "POST":
        
        first_name = request.POST.get('name')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        check_email = utils.check_email(email)   
            
        # check_password_messages = utils.check_password(password, password2)
        
        if check_email:
            messages.error(request,"O email ja esta cadastrado")
            return redirect("user:register")
        
        # if check_password_messages:
        #     for password_message in check_password_messages: 
        #         messages.error(request, password_message)
                
        #     return redirect(reverse("user:register"))
        
        user = CustomUser.objects.create_user(first_name=first_name, last_name=lastname, email=email)
        user.set_password(password)
        user.save()
        try:
            login(request, user)
            
            return redirect("jobs:index")
        except:
            messages.error(request,"Não foi possivel realizar o login. Tente novamente")
            pass
 
    return render(request,"user/register.html")

def edit_user(request):
    user = request.user

    if request.method == "POST":
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"Usuário alterado com sucesso")
            
            return redirect("user:view_user")
        else:
            messages.error(request, "Algo deu errado! Tente novamente")
            pass
    form = CustomUserForm(instance=user)
    
    context ={
        "form":form
    }
    return render(request, "user/edit_user.html", context)

def view_user(request):

    user = request.user
    context ={
        "user":user
    }
    
    return render(request, "user/view_user.html", context)


def login_view(request):
    
    
    if request.method == "POST":
        print(request)
                
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            try:
                login(request, user)
            
                return redirect("jobs:index")
            except:
                messages.error(request,"Não foi possivel realizar o login. Tente novamente.")
                return redirect("user:login_view")
        
        else:
            messages.error(request,"Email e/ou Senha Invalida")
            return redirect("user:login_view")
            
            
    return render (request, 'user/register.html',)

def logout_view(request):
    
    logout(request)

    return  HttpResponseRedirect(reverse("jobs:index"))