# Generated by Django 4.1.3 on 2022-12-09 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orion', '0010_alter_ordem_servico_descricao_servico_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipamento',
            name='descricao',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
