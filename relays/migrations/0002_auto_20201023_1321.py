# Generated by Django 3.1.2 on 2020-10-23 13:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relays', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relayconfigurations',
            name='token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relays.accesstokens'),
        ),
    ]