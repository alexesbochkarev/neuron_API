# Generated by Django 4.2 on 2023-07-20 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_result_options_alter_tool_options_whitelist_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='privacy',
            name='interests',
            field=models.BooleanField(default=False, verbose_name='Interests'),
        ),
    ]
