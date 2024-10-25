from django.db import models
from user.models import CustomUser
# Create your models here.

class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        abstract = True
        
class CandidateProfile(Location):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    personal_sumary = models.TextField(null=True, blank=True)
    professional_sumary = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return f'{self.user.first_name} {self.user.last_name}'

class CompanyProfile(Location):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="companies")    
    company_name = models.CharField(max_length=150)
    resume_company = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.company_name}'
    
class Vacancies(Location):
    TYPES_CONTRACT_CHOICES = {
        "clt":"CLT",
        "temporario":"Temporario",
        "freelance":"Freelance"
    }
    
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name="vacancies")
    title = models.CharField(max_length=150)    
    descript = models.TextField()
    contract_type = models.CharField(max_length=150, choices=TYPES_CONTRACT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Company: {self.company.company_name} - Title: {self.title}'