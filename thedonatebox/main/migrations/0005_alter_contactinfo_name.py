# Generated by Django 4.1.12 on 2024-04-17 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_contactinfo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
