# Generated by Django 5.1.2 on 2024-10-25 19:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0002_companyprofile_company_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="candidateprofile",
            name="personal_sumary",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="candidateprofile",
            name="professional_sumary",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="vacancies",
            name="contract_type",
            field=models.CharField(
                choices=[
                    ("clt", "CLT"),
                    ("temporario", "Temporário"),
                    ("freelance", "Freelance"),
                ],
                max_length=150,
            ),
        ),
    ]
