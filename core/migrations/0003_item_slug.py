# Generated by Django 2.2.5 on 2020-06-11 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200527_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='slugfield'),
            preserve_default=False,
        ),
    ]
