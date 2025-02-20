# Generated by Django 5.1.1 on 2024-09-09 17:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("central", "0002_alter_cuidador_endereco_alter_paciente_endereco_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="turno",
            name="cuidador",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cuidador",
                to="central.cuidador",
            ),
        ),
        migrations.AlterField(
            model_name="turno",
            name="paciente",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="paciente",
                to="central.paciente",
            ),
        ),
    ]
