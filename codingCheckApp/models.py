from django.db import models
from django.utils import timezone
import datetime

language_list = (("python", "python"),)
method_list = (("equality", "="), ("estimation", "<"),)
difficulty_list = (("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"))
upload_date = datetime.datetime.now().strftime("codes/%Y-%m-%d")

class Category(models.Model):

    title = models.CharField(verbose_name='カテゴリ', max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Post(models.Model):

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='タイトル', max_length=200)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)

    problem_text = models.TextField(verbose_name='問題文', blank=True, null=True, max_length=1000)
    input_text = models.TextField(verbose_name='入力説明', blank=True, null=True, max_length=1000)
    input_code = models.TextField(verbose_name='入力例', blank=True, null=True, max_length=1000, default=None)
    output_text = models.TextField(verbose_name='出力説明', blank=True, null=True, max_length=1000)
    output_code = models.TextField(verbose_name='出力例', blank=True, null=True, max_length=1000, default=None)

    sample_input1 = models.TextField(verbose_name='入力サンプル1', blank=True, null=True, max_length=10000)
    sample_output1 = models.TextField(verbose_name='出力サンプル1', blank=True, null=True, max_length=10000)
    sample_input2 = models.TextField(verbose_name='入力サンプル2', blank=True, null=True, max_length=10000)
    sample_output2 = models.TextField(verbose_name='出力サンプル2', blank=True, null=True, max_length=10000)
    sample_input3 = models.TextField(verbose_name='入力サンプル3', blank=True, null=True, max_length=10000)
    sample_output3 = models.TextField(verbose_name='出力サンプル3', blank=True, null=True, max_length=10000)
    sample_input4 = models.TextField(verbose_name='入力サンプル４', blank=True, null=True, max_length=10000)
    sample_output4 = models.TextField(verbose_name='出力サンプル4', blank=True, null=True, max_length=10000)
    sample_input5 = models.TextField(verbose_name='入力サンプル5', blank=True, null=True, max_length=10000)
    sample_output5 = models.TextField(verbose_name='出力サンプル5', blank=True, null=True, max_length=10000)

    difficulty = models.CharField(max_length=5, choices=difficulty_list, verbose_name='難易度', default=difficulty_list[0][0])

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

class Score(models.Model):

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    score = models.FloatField(verbose_name="スコア", blank=True, null=True)

    def __str__(self):
        return self.post.title