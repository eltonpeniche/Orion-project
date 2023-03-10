# Generated by Django 4.1.3 on 2023-02-28 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orion', '0024_cargahoraria_horas_de_trabalho'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargahoraria',
            name='horas_de_trabalho',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='endereco',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='empresa', to='orion.endereco'),
        ),
    ]
