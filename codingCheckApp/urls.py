from django.urls import path
from . import views

urlpatterns = [
    path('', views.Main, name='main'),
    path('post_list/', views.PostList, name='post_list'),
    path('post/<int:pk>/', views.PostDetail, name='post_detail'),
    path('post/<int:pk>/submit_code', views.PostDetail, name='submit_code'),
    path('post/<int:pk>/submit_sample/', views.SubmitSample, name='submit_sample'),
    path('post/<int:pk>/ranking', views.Ranking, name='ranking'),
]