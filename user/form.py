from .models import CustomUser
from django.forms import ModelForm

class CustomUserForm(ModelForm):
    class Meta:
        
        model = CustomUser
        fields = ["first_name","last_name", "email"]