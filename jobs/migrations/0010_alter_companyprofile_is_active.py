# Generated by Django 5.1.2 on 2025-01-01 13:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0009_companyprofile_is_deleted_vacancies_show_company"),
    ]

    operations = [
        migrations.AlterField(
            model_name="companyprofile",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]
