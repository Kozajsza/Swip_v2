# Generated by Django 4.0.4 on 2022-07-30 12:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('SWIPapp', '0007_lists'),
    ]

    operations = [
        migrations.AddField(
            model_name='lists',
            name='Created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]