# Generated by Django 3.0.7 on 2020-12-27 22:44

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0005_auto_20201222_1930"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="post", managers=[("live_posts", django.db.models.manager.Manager()),],
        ),
    ]
