# Generated by Django 4.1.3 on 2023-02-24 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_alter_usuario_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipo',
            field=models.CharField(choices=[('A', 'Admin'), ('T', 'Tecnico')], default='T', max_length=1),
        ),
    ]