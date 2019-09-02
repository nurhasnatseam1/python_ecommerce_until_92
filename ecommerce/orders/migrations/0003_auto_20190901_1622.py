# Generated by Django 2.2.4 on 2019-09-01 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
        ('orders', '0002_auto_20190901_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='billing.BillingProfile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='order',
            field=models.BooleanField(default=True),
        ),
    ]
