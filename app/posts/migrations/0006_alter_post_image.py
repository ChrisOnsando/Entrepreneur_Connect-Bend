# Generated by Django 4.2.5 on 2023-10-25 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.TextField(null=True),
        ),
    ]