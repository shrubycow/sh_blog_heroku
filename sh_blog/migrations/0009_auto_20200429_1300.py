# Generated by Django 3.0.5 on 2020-04-29 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sh_blog', '0008_auto_20200428_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
