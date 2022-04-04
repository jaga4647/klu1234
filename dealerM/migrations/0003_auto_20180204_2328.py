# Generated by Django 2.0.2 on 2018-02-04 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dealerM', '0002_wholesaledeal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wholesaledeal',
            name='dealer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dealerM.Dealer'),
        ),
        migrations.AlterField(
            model_name='wholesaledeal',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manufacturerM.Manufacturer'),
        ),
    ]
