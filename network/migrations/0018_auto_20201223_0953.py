# Generated by Django 3.1.2 on 2020-12-23 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0017_auto_20201222_1611'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='liking',
            name='like',
        ),
        migrations.AddField(
            model_name='liking',
            name='preference',
            field=models.CharField(choices=[('Like', 'Like'), ('Dislike', 'Dislike')], default='Like', max_length=7, null=True),
        ),
    ]