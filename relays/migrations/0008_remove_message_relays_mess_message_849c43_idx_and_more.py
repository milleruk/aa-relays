# Generated by Django 4.0.10 on 2023-06-16 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relays', '0007_alter_message_user'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='message',
            name='relays_mess_message_849c43_idx',
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['message', 'channel'], name='relays_mess_message_29ecba_idx'),
        ),
    ]