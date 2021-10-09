# Generated by Django 3.2.4 on 2021-10-07 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20211008_0052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addinfo',
            name='id',
        ),
        migrations.RemoveField(
            model_name='addinfo',
            name='user',
        ),
        migrations.AddField(
            model_name='addinfo',
            name='email',
            field=models.EmailField(default='', max_length=254, primary_key=True, serialize=False),
        ),
    ]
