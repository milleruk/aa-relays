# Generated by Django 4.0.10 on 2023-06-16 05:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relays', '0006_auto_20230616_0450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relays.user', verbose_name=''),
        ),
    ]
