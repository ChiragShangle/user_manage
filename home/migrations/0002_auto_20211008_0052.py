# Generated by Django 3.2.4 on 2021-10-07 19:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='auth_token',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='forget_password_token',
        ),
        migrations.AddField(
            model_name='profile',
            name='otp',
            field=models.CharField(default='', max_length=6),
        ),
        migrations.CreateModel(
            name='Addinfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=60)),
                ('address', models.CharField(max_length=60)),
                ('city', models.CharField(max_length=60)),
                ('pin', models.IntegerField()),
                ('officeno', models.CharField(max_length=10)),
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]