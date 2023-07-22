# Generated by Django 4.2 on 2023-07-21 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tariffs', '0010_tariff_stripecustomerid_tariff_stripesubscriptionid_and_more'),
        ('oauth', '0006_user_renew_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tariff',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='tariffs.tariff'),
        ),
    ]
