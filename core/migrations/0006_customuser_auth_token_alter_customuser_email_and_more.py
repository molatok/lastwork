# Generated by Django 4.1.7 on 2023-04-27 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_rename_user_customuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="auth_token",
            field=models.CharField(max_length=40, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="first_name",
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="last_name",
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="username",
            field=models.CharField(max_length=150, unique=True),
        ),
    ]