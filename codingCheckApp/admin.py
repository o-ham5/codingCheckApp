from django.contrib import admin
from .models import Post, Category, Score


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Score)