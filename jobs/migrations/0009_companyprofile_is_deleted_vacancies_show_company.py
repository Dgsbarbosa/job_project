# Generated by Django 5.1.2 on 2024-11-03 19:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0008_companyprofile_is_active_vacancies_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="companyprofile",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="vacancies",
            name="show_company",
            field=models.BooleanField(default=True),
        ),
    ]
