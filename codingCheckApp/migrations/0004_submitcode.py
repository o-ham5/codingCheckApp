# Generated by Django 2.2.2 on 2020-04-07 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codingCheckApp', '0003_auto_20200407_2031'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmitCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(blank=True, choices=[('python', 'python')], max_length=20, null=True, verbose_name='使用言語')),
                ('file', models.FileField(upload_to='codes/', verbose_name='コード')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
