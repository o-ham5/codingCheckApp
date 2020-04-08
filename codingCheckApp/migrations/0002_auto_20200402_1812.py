# Generated by Django 2.2.2 on 2020-04-02 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codingCheckApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='input_code',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='post',
            name='input_text',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='post',
            name='language',
            field=models.CharField(blank=True, choices=[('python', 'python')], max_length=20, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='post',
            name='output_code',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='post',
            name='output_text',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='post',
            name='sample_input1',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='post',
            name='sample_input2',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='post',
            name='sample_input3',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='post',
            name='sample_input4',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='post',
            name='sample_input5',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='post',
            name='sample_output1',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='post',
            name='sample_output2',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='post',
            name='sample_output3',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='post',
            name='sample_output4',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='post',
            name='sample_output5',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='problem_text',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name=''),
        ),
    ]
