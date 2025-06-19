from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.home, name='home'),
    # Move create above detail
    path('article/create/', views.article_create, name='article_create'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('category/<int:category_id>/', views.category_view, name='category'),
    path('search/', views.search, name='search'),
    # NEW: article update
    path('article/<slug:slug>/edit/', views.article_update, name='article_update'),
    # NEW: article delete
    path('article/<slug:slug>/delete/', views.article_delete, name='article_delete'),
]