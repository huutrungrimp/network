# Generated by Django 3.1.2 on 2020-12-13 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_user_bio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='body',
            new_name='content',
        ),
    ]
