# Generated by Django 3.1.2 on 2020-12-22 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0014_remove_post_likes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Preference',
            new_name='Liking',
        ),
        migrations.RenameField(
            model_name='liking',
            old_name='preference_status',
            new_name='preference',
        ),
    ]
