# Generated by Django 4.2.5 on 2023-10-25 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_remove_post_author_remove_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
    ]
