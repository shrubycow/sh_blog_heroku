# Generated by Django 3.0.5 on 2020-04-28 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sh_blog', '0006_auto_20200420_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.CharField(max_length=250),
        ),
    ]
