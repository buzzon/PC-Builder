# Generated by Django 3.1.3 on 2020-12-16 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcbknowledge', '0013_auto_20201216_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='build',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]