# Generated by Django 4.1.7 on 2023-04-08 00:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("stockmanage", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="moneymanage",
            new_name="stockmanage",
        ),
    ]