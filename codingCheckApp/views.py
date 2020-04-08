from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.files.storage import FileSystemStorage

from .models import Post, upload_date
from .forms import SubmitCodeForm

import subprocess

def Main(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'codingCheckApp/main.html', {'posts': posts})

def PostList(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'codingCheckApp/post_list.html', {'posts': posts})

def PostDetail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = SubmitCodeForm()
    
    if request.method == "POST":
        form = SubmitCodeForm(request.POST, request.FILES)
        if form.is_valid():

            book = form.save(commit=False)
            book.save()

            file = request.FILES['file']
            file_path = f"media/{upload_date}/{file.name}"

            # fileobject = FileSystemStorage()
            # fileobject.save(f"codes/{file.name}", file)

            inputs = [post.sample_input1, post.sample_input2, post.sample_input3, post.sample_input4, post.sample_input5]
            outputs = [post.sample_output1, post.sample_output2, post.sample_output3, post.sample_output4, post.sample_output5]
            judges = []
            result_outputs = []

            for k, inp in enumerate(inputs):
                inp = inp.split("\n")
                exe_cmd_shell = "("
                for line in inp:
                    exe_cmd_shell += f"echo {line};"
                exe_cmd_shell += f") | python {file_path}"
                result = subprocess.run(exe_cmd_shell, shell=True, stdout=subprocess.PIPE)
                result_output = result.stdout.decode("utf8").strip()
                judges.append(outputs[k] == result_output)
                result_outputs.append(result_output)

            return render(request, "codingCheckApp/submit_code.html", {'post': post, 'results': enumerate(judges), 'outputs': result_outputs})
    return render(request, 'codingCheckApp/post_detail.html', {'post': post, 'form': form})