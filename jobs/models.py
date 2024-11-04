from django.db import models
from user.models import CustomUser
# Create your models here.

class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        abstract = True

class Contact(models.Model):
    phone1 = models.CharField(max_length=25, null=True, blank=True)
    phone2 = models.CharField(max_length=25, null=True, blank=True)    
    email = models.EmailField(null=True, blank=True)
  
    class Meta:
        abstract = True
        
class CandidateProfile(Contact,Location):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    personal_sumary = models.TextField(null=True, blank=True)
    professional_sumary = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return f'{self.user.first_name} {self.user.last_name}'

class CompanyProfile(Contact,Location):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="companies")    
    company_name = models.CharField(max_length=150)
    resume_company = models.TextField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.company_name}'
    
class Vacancies(Contact,Location):
    TYPES_CONTRACT_CHOICES = [
        ("clt", "CLT"),
        ("temporario", "Temporário"),
        ("freelance", "Freelance")
    ]
    
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name="vacancies")
    title = models.CharField(max_length=150)    
    descript = models.TextField()
    contract_type = models.CharField(max_length=150, choices=TYPES_CONTRACT_CHOICES)
    is_active = models.BooleanField(default=True)
    show_company = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Company: {self.company.company_name} - Title: {self.title}'
    
class SaveVacancy(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="saved_vacancies")
    vacancy = models.ForeignKey(Vacancies,on_delete=models.CASCADE,related_name="saved_by_user")
    saved_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user} - {self.vacancy.title}'