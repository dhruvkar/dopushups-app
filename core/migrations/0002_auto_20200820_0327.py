# Generated by Django 3.1 on 2020-08-20 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='challenger',
            options={'verbose_name_plural': 'challengers'},
        ),
        migrations.AlterModelOptions(
            name='exercise',
            options={'verbose_name_plural': 'exercises'},
        ),
        migrations.AlterModelTable(
            name='challenger',
            table='challenger',
        ),
        migrations.AlterModelTable(
            name='exercise',
            table='exercise',
        ),
    ]
