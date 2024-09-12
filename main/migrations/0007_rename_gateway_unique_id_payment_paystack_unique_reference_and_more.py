# Generated by Django 5.1 on 2024-09-12 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_payment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='gateway_unique_id',
            new_name='paystack_unique_reference',
        ),
        migrations.AddField(
            model_name='payment',
            name='stripe_intent',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
