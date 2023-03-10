# Generated by Django 4.1.3 on 2023-03-12 03:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("orion", "0031_endereco_complemento"),
    ]

    operations = [
        migrations.CreateModel(
            name="Despesa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tipo",
                    models.CharField(
                        choices=[
                            ("AL", "Alimentação"),
                            ("BA", "Bagagem"),
                            ("AC", "Aluguel de carros"),
                            ("CO", "Combustível"),
                            ("CF", "Correio/Frete"),
                            ("ES", "Estacionamento"),
                            ("FR", "Friogobar"),
                            ("HO", "Hospedagem"),
                            ("LA", "Lavanderia"),
                            ("CM", "Compra de material"),
                            ("PG", "Pagamentos"),
                            ("PA", "Passagem Aéria"),
                            ("TR", "Transporte"),
                            ("OT", "Outros"),
                        ],
                        default="AL",
                        max_length=2,
                    ),
                ),
                ("data", models.DateField()),
                ("valor", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "ordem_servico",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="despesa",
                        to="orion.ordem_servico",
                    ),
                ),
            ],
        ),
    ]
