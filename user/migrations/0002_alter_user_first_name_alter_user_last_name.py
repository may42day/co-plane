# Generated by Django 4.1.3 on 2022-12-04 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, default='123', max_length=150, verbose_name='first name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, default='123', max_length=150, verbose_name='last name'),
            preserve_default=False,
        ),
    ]