
  

from django.core.exceptions import ValidationError
import django
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_project.settings')
django.setup()

from django.conf import settings
import requests
import json
from datetime import datetime, timedelta



def validate_phone(phone):
    if not phone.is_digit():
        raise ValidationError("O telefone deve conter apenas números.")
    

CACHE_FILE = "locations.json"  # Nome do arquivo local
CACHE_EXPIRATION_DAYS = 90  # Expiração em dias (3 meses)

def load_cache():
    """Carrega o cache do arquivo local."""
    if not os.path.exists(CACHE_FILE):
        return None
    with open(CACHE_FILE, "r") as file:
        return json.load(file)

def save_cache(data):
    """Salva os dados no arquivo local."""
    with open(CACHE_FILE, "w") as file:
        json.dump(data, file)

def is_cache_expired():
    """Verifica se o cache está expirado."""
    if not os.path.exists(CACHE_FILE):
        return True
    file_mod_time = datetime.fromtimestamp(os.path.getmtime(CACHE_FILE))
    return datetime.now() - file_mod_time > timedelta(days=CACHE_EXPIRATION_DAYS)

def fetch_data_from_api(url):
    """Faz uma chamada para a API e retorna os dados."""
    headers = {
        'X-CSCAPI-KEY': settings.COUNTRYSTATECITY_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None