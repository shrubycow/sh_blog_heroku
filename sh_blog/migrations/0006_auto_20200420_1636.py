# Generated by Django 3.0.5 on 2020-04-20 16:36

from django.db import migrations, models
import sh_blog.models


class Migration(migrations.Migration):

    dependencies = [
        ('sh_blog', '0005_auto_20200420_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to=sh_blog.models.user_media_path),
        ),
    ]
