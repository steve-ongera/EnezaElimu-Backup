# Generated by Django 5.1.2 on 2025-02-04 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_newsupdate_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile.png', null=True, upload_to='students_profiles/'),
        ),
    ]
