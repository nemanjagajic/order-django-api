# Generated by Django 3.0.3 on 2020-02-03 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200203_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, default='nemanja@mailinator.com', max_length=254, verbose_name='email address'),
            preserve_default=False,
        ),
    ]
