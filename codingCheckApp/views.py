from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

from .models import Category, Post, method_list, Score
from .forms import SubmitCodeForm

import subprocess
import datetime

def Main(request):

    return render(request, 'codingCheckApp/main.html')

@login_required
def CategoryList(request):
    categorys = Category.objects.all().order_by("created_date").reverse()

    cat2date = {}
    for category in categorys:
        posts = Post.objects.filter(category=category).order_by("published_date").reverse()
        last_updated = posts[0].published_date
        cat2date[category] = last_updated

    return render(request, 'codingCheckApp/category_list.html', {'categorys': cat2date})
    


@login_required
def PostList(request, category_pk):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    user = request.user

    scores = []
    for post in posts:
        score_model = Score.objects.filter(user=user, post=post)[0]
        score = score_model.score
        scores.append(score)

    return render(request, 'codingCheckApp/post_list.html', {'posts_scores': zip(posts, scores)})
    
@login_required
def PostDetail(request, post_pk, category_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = SubmitCodeForm()
    user = request.user
    
    # コード提出後
    if request.method == "POST":
        form = SubmitCodeForm(request.POST, request.FILES)
        if form.is_valid():

            # book = form.save(commit=False)
            # book.save()

            # ファイル保存先
            file = request.FILES['file']
            today = str(datetime.date.today())
            today_time = str(datetime.datetime.now().time()).replace(':', '.')
            file_path = f"codes/{user}/{post_pk}/{today}/{today_time}/{file.name}"

            # {project_ROOT}/media/codes/{username}/{pk}/{today}/{now}/{filename}としてここで直接保存 (models.pyでは定義していない)
            # 例: media/codes/admin/1/2020-01-01/07.42.44.400874/tmp.py
            fileobject = FileSystemStorage()
            fileobject.save(file_path, file)

            inputs = [post.sample_input1, post.sample_input2, post.sample_input3, post.sample_input4, post.sample_input5]
            outputs = [post.sample_output1, post.sample_output2, post.sample_output3, post.sample_output4, post.sample_output5]
            judges = []
            result_outputs = []

            # とりあえずpythonのみ
            if request.POST["language"] == "python":
                # サブプロセスにて実行
                for k, inp in enumerate(inputs):
                    inp = inp.split("\n")
                    exe_cmd_shell = "("
                    for line in inp:
                        exe_cmd_shell += f"echo {line};"
                    exe_cmd_shell += f") | python media/{file_path}"
                    p = subprocess.Popen(exe_cmd_shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout_data, stderr_data = p.communicate()
                    stdout_data, stderr_data = stdout_data.decode("utf8").strip(), stderr_data.decode("utf8").strip()
                    result_output = stdout_data

                    # 結果処理
                    if post.method == method_list[0][0]:  # equality
                        judge = outputs[k] == result_output
                    elif post.method == method_list[1][0]:  # estimation
                        judge = float(outputs[k]) - float(result_output) < post.tolerable_error
                    judges.append(judge)
                    if not judge and stderr_data:
                        result_output = stderr_data
                    result_outputs.append(result_output)

            # スコア更新
            score = calc_score(post.method, judges)
            score_model = Score.objects.filter(user=user, post=post)
            if len(score_model) == 0:
                Score.objects.create(user=user, post=post, score=score)
            elif len(score_model) == 1:
                if score_model[0].score < score:
                    score_model[0].score = score
                    score_model[0].save()

            return render(request, "codingCheckApp/submit_code.html", {'post': post, 'results': enumerate(judges), 'outputs': result_outputs, 'user': user})
    return render(request, 'codingCheckApp/post_detail.html', {'post': post, 'form': form, 'user': user,})


@login_required
def SubmitSample(request, post_pk, category_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = SubmitCodeForm()
    user = request.user
    
    # コード提出後
    if request.method == "POST":
        form = SubmitCodeForm(request.POST, request.FILES)
        if form.is_valid():

            # book = form.save(commit=False)
            # book.save()

            # ファイル保存先
            file = request.FILES['file']
            today = str(datetime.date.today())
            today_time = str(datetime.datetime.now().time()).replace(':', '.')
            file_path = f"codes/{user}/{post_pk}/example/{today}/{today_time}/{file.name}"

            # {project_ROOT}/media/codes/{username}/{pk}/example/{today}/{now}/{filename}としてここで直接保存 (models.pyでは定義していない)
            # 例: media/codes/admin/1/example/2020-01-01/07.42.44.400874/tmp.py
            fileobject = FileSystemStorage()
            fileobject.save(file_path, file)

            inp = post.sample_input1
            outp = post.sample_output1

            # とりあえずpythonのみ
            if request.POST["language"] == "python":
                
                # サブプロセスにて実行
                inp = inp.split("\n")
                exe_cmd_shell = "("
                for line in inp:
                    exe_cmd_shell += f"echo {line};"
                exe_cmd_shell += f") | python media/{file_path}"
                p = subprocess.Popen(exe_cmd_shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout_data, stderr_data = p.communicate()
                stdout_data, stderr_data = stdout_data.decode("utf8").strip(), stderr_data.decode("utf8").strip()

                if stderr_data:
                    result = stderr_data
                else:
                    result = stdout_data
                
                data = {
                    'e_output': outp,
                    'result': result,
                    'inp': "<br>".join(inp).replace("\r", ""),
                    'error': False,
                }
                    

            return JsonResponse(data)

        inp = post.sample_input1
        outp = post.sample_output1

        data = {
            'inp': "<br>".join(inp.split("\n")).replace("\r", ""),
            'e_output': outp,
            'result': 'None',
            'error': True
        }
        
        return JsonResponse(data)

def Ranking(request, post_pk, category_pk):

    post = get_object_or_404(Post, pk=post_pk)
    scores = Score.objects.filter(post=post).order_by("-score")

    return render(request, 'codingCheckApp/ranking.html', {'post': post, 'scores': enumerate(scores)})

def calc_score(method, output):
    """
    method == "equality"なら正解率
    method == "estimation"なら誤差平均
    が最終的なスコアとする
    """
    if method == "equality":
        acc_rate = int((sum([1 for b in output if b]) / len(output)) *100)

    if method == "estimation":
        pass


    return acc_rate