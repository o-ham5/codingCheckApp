from django.urls import path
from . import views

urlpatterns = [
    path('', views.Main, name='main'),
    path('category_list/', views.CategoryList, name='category_list'),
    path('category<int:category_pk>/post_list/', views.PostList, name='post_list'),
    path('category<int:category_pk>/post<int:post_pk>/', views.PostDetail, name='post_detail'),
    path('category<int:category_pk>/post<int:post_pk>/submit_code', views.PostDetail, name='submit_code'),
    path('category<int:category_pk>/post<int:post_pk>/submit_sample/', views.SubmitSample, name='submit_sample'),
    path('category<int:category_pk>/post<int:post_pk>/ranking', views.Ranking, name='ranking'),
]