# Generated by Django 4.1.3 on 2023-03-04 14:00

from django.db import migrations, models
import jsignature.fields


class Migration(migrations.Migration):

    dependencies = [
        ('orion', '0028_alter_ordem_servico_equipamento'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignatureModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', jsignature.fields.JSignatureField()),
            ],
        ),
    ]
