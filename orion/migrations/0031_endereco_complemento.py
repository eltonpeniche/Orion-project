# Generated by Django 4.1.3 on 2023-03-09 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orion", "0030_ordem_servico_assinatura"),
    ]

    operations = [
        migrations.AddField(
            model_name="endereco",
            name="complemento",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]