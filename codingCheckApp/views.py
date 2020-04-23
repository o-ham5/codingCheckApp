from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

from .models import Post, method_list
from .forms import SubmitCodeForm

import subprocess
import datetime

def Main(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'codingCheckApp/main.html', {'posts': posts})

@login_required
def PostList(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'codingCheckApp/post_list.html', {'posts': posts})
    
@login_required
def PostDetail(request, pk):
    post = get_object_or_404(Post, pk=pk)
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
            file_path = f"codes/{user}/{pk}/{today}/{today_time}/{file.name}"

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

            return render(request, "codingCheckApp/submit_code.html", {'post': post, 'results': enumerate(judges), 'outputs': result_outputs, 'user': user})
    return render(request, 'codingCheckApp/post_detail.html', {'post': post, 'form': form, 'user': user,})


@login_required
def submit_sample(request, pk):
    post = get_object_or_404(Post, pk=pk)
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
            file_path = f"codes/{user}/{pk}/example/{today}/{today_time}/{file.name}"

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

        data = {
            'error': True
        }
        
        return JsonResponse(data)