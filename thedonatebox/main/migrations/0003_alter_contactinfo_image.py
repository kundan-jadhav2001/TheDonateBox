# Generated by Django 4.1.12 on 2024-04-16 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_contactinfo_delete_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='image',
            field=models.ImageField(upload_to='media'),
        ),
    ]
