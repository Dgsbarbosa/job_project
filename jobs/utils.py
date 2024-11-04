
  
from django.core.exceptions import ValidationError


def validate_phone(phone):
    if not phone.is_digit():
        raise ValidationError("O telefone deve conter apenas números.")
    
