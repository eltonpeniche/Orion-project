# Generated by Django 4.1.3 on 2022-12-10 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orion', '0011_alter_equipamento_descricao'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contato',
            old_name='nome',
            new_name='nomeContato',
        ),
    ]
