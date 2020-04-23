from django import forms
from .models import Post, SubmitCode, language_list


class PostForm(forms.ModelForm):

    class Meta:                       
        model = Post                  # 使うモデルを指定
        fields = ('title', 
        'problem_text', 
        'input_text', 
        'input_code', 
        'output_text', 
        'output_code', 
        'sample_input1', 
        'sample_output1', 
        'sample_input2', 
        'sample_output2', 
        'sample_input3', 
        'sample_output3', 
        'sample_input4', 
        'sample_output4', 
        'sample_input5', 
        'sample_output5')
        # widgets = {
        #     'text': forms.Textarea(attrs={'placeholder': 'Markdown形式で書いてください。'})
        # }

class SubmitCodeForm(forms.ModelForm):

    # <input>, <select>タグにform属性を入れるための処理
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'form': 'submit-code'})
    )
    language = forms.CharField(
        widget=forms.Select(attrs={'form': 'submit-code'}, choices=language_list)
    )
    class Meta:
        model = SubmitCode
        fields = ('language', 'file', )
        widgets = {
            # 'language': forms.CharField(attrs={'id': 'submit-code'}),
        }