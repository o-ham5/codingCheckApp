# Generated by Django 2.1 on 2020-04-18 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codingCheckApp', '0006_auto_20200418_0645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tolerable_error',
            field=models.FloatField(blank=True, null=True, verbose_name='許容誤差'),
        ),
    ]