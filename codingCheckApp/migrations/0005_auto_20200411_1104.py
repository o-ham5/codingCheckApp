# Generated by Django 2.1 on 2020-04-11 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codingCheckApp', '0004_submitcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submitcode',
            name='file',
            field=models.FileField(upload_to='codes/2020-04-11', verbose_name='コード'),
        ),
    ]
