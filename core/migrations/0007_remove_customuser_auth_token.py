# Generated by Django 4.1.7 on 2023-04-27 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_customuser_auth_token_alter_customuser_email_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="auth_token",
        ),
    ]