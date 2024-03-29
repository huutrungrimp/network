# Generated by Django 3.1.2 on 2020-12-22 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_post_preference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='preference',
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference_status', models.CharField(choices=[('Like', 'Like'), ('Dislike', 'Dislike')], default='Like', max_length=7, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.post')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
