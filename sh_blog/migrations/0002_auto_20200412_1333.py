# Generated by Django 3.0.5 on 2020-04-12 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sh_blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='greeting',
            name='when',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date created'),
        ),
    ]
