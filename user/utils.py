import re
from .models import CustomUser

def check_email(email):
    user = CustomUser.objects.filter(email=email)
    
    return user


def check_password(password, confirm_password):
    
    messages = []
    if password != confirm_password:
            messages.append("As senhas precisam ser iguais.")
            
    if len(password) < 8:
        messages.append("A senha deve ter pelo menos de 8 caracteres.")
    if not re.findall(r'[A-Z]',password):
        messages.append("A senha deve ter pelo menos uma letra maiúscula.")
        
    if not re.findall(r'[a-z]',password):
        messages.append("A senha deve ter pelo menos uma letra minúscula.")
    if not re.findall(r'[0-9]',password):
        messages.append("A senha deve ter pelo menos um numero.")
    
    if not re.findall(r'[\W]',password):
        messages.append('A senha deve conter pelo menos um caractere.')
    
    return messages
