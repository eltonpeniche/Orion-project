# Generated by Django 4.1.3 on 2023-03-11 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orion", "0032_despesa"),
    ]

    operations = [
        migrations.AlterField(
            model_name="despesa",
            name="valor",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
