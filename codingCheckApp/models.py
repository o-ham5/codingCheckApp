from django.db import models
from django.utils import timezone
import datetime

language_list = (("python", "python"),)
method_list = (("equality", "="), ("estimation", "<"),)
upload_date = datetime.datetime.now().strftime("codes/%Y-%m-%d")

class Post(models.Model):

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='タイトル', max_length=200)

    problem_text = models.TextField(verbose_name='問題文', blank=True, null=True, max_length=1000)
    input_text = models.TextField(verbose_name='入力説明', blank=True, null=True, max_length=1000)
    input_code = models.TextField(verbose_name='入力例', blank=True, null=True, max_length=1000, default=None)
    output_text = models.TextField(verbose_name='出力説明', blank=True, null=True, max_length=1000)
    output_code = models.TextField(verbose_name='出力例', blank=True, null=True, max_length=1000, default=None)

    sample_input1 = models.TextField(verbose_name='入力サンプル1', blank=True, null=True, max_length=1000)
    sample_output1 = models.TextField(verbose_name='出力サンプル1', blank=True, null=True, max_length=1000)
    sample_input2 = models.TextField(verbose_name='入力サンプル2', blank=True, null=True, max_length=1000)
    sample_output2 = models.TextField(verbose_name='出力サンプル2', blank=True, null=True, max_length=1000)
    sample_input3 = models.TextField(verbose_name='入力サンプル3', blank=True, null=True, max_length=1000)
    sample_output3 = models.TextField(verbose_name='出力サンプル3', blank=True, null=True, max_length=1000)
    sample_input4 = models.TextField(verbose_name='入力サンプル４', blank=True, null=True, max_length=1000)
    sample_output4 = models.TextField(verbose_name='出力サンプル4', blank=True, null=True, max_length=1000)
    sample_input5 = models.TextField(verbose_name='入力サンプル5', blank=True, null=True, max_length=1000)
    sample_output5 = models.TextField(verbose_name='出力サンプル5', blank=True, null=True, max_length=1000)

    method = models.CharField(max_length=20, choices=method_list, verbose_name='判定基準', default=method_list[0][0])

    tolerable_error = models.FloatField(verbose_name="許容誤差", blank=True, null=True)

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


    def publish(self):
        self.published_date = timezone.now()    
        self.save()


    def __str__(self):
        return self.title

class SubmitCode(models.Model):

    language = models.CharField(max_length=20, choices=language_list, verbose_name='使用言語', blank=True, null=True)
    # file = models.FileField(verbose_name='コード', upload_to=upload_date)
    file = models.FileField(verbose_name='コード')
    uploaded_at = models.DateTimeField(auto_now_add=True)