# Generated by Django 4.2.9 on 2024-02-06 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('otp', models.CharField(max_length=100)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
