# Generated by Django 2.2 on 2019-11-20 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20191120_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='tienda',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.Tienda'),
        ),
        migrations.AlterField(
            model_name='productoventa',
            name='cantidad',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='productoventa',
            name='valor_unidad',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
