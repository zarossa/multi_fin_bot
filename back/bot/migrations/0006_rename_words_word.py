# Generated by Django 4.1.7 on 2023-04-19 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Words',
            new_name='Word',
        ),
    ]