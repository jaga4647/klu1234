# Generated by Django 2.0.2 on 2018-02-04 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturerM', '0003_auto_20180204_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufactureinventory',
            name='count',
            field=models.IntegerField(null=True),
        ),
    ]