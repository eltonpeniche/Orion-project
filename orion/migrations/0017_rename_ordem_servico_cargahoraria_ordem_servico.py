# Generated by Django 4.1.3 on 2022-12-14 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orion', '0016_remove_cargahoraria_ordem_servico_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cargahoraria',
            old_name='ordem_Servico',
            new_name='ordem_servico',
        ),
    ]
