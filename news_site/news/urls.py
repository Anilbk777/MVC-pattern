from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('category/<int:category_id>/', views.category_view, name='category'),
    path('search/', views.search, name='search'),
]