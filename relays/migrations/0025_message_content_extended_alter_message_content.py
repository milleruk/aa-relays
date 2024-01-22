# Generated by Django 4.0.10 on 2023-06-14 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relays', '0024_rename_end_time_event_end_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='content_extended',
            field=models.TextField(default='', help_text='Additional Content, Embeds, URLs, Attachments etc'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.TextField(help_text='The primary content of a message'),
        ),
    ]
