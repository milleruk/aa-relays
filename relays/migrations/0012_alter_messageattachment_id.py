# Generated by Django 4.0.10 on 2023-06-19 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relays', '0011_rename_event_relayconfiguration_relay_event_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageattachment',
            name='id',
            field=models.PositiveBigIntegerField(primary_key=True, serialize=False, verbose_name=''),
        ),
    ]