# Generated by Django 4.1.3 on 2023-03-03 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_alter_usuario_tipo'),
        ('orion', '0025_alter_cargahoraria_horas_de_trabalho_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='email',
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='observacao',
            field=models.CharField(blank=True, max_length=280, null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='telefone',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='descricao',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipamento', to='orion.empresa'),
        ),
        migrations.AlterField(
            model_name='ordem_servico',
            name='aberto_por',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordem_servico', to='usuarios.usuario'),
        ),
        migrations.AlterField(
            model_name='ordem_servico',
            name='empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordem_servico', to='orion.empresa'),
        ),
    ]