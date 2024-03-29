# Generated by Django 4.0.10 on 2023-06-12 10:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aadiscordbot', '0009_alter_quotemessage_options'),
        ('relays', '0005_rename_datetime_messages_timestamp_messages_deleted_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relayconfigurations',
            name='token',
        ),
        migrations.AlterField(
            model_name='destinationaadiscordbot',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aadiscordbot.channels'),
        ),
        migrations.AlterField(
            model_name='relayconfigurations',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
