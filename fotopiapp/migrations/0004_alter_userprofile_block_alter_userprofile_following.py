# Generated by Django 5.0.4 on 2024-08-18 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fotopiapp', '0003_alter_userprofile_profil_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='block',
            field=models.ManyToManyField(blank=True, related_name='blocked', to='fotopiapp.userprofile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='followed_by', to='fotopiapp.userprofile'),
        ),
    ]
