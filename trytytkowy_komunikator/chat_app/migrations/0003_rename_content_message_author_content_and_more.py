# Generated by Django 4.1.5 on 2023-01-26 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0002_alter_message_author_delete_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='content',
            new_name='author_content',
        ),
        migrations.AddField(
            model_name='message',
            name='receiver_content',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]