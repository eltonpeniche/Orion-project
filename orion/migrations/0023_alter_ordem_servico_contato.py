# Generated by Django 4.1.3 on 2023-02-22 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orion', '0022_remove_empresa_contato_alter_ordem_servico_contato_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordem_servico',
            name='contato',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
