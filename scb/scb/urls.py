"""
Маршрутизаторы приложения.
"""

from django.contrib import admin
from django.urls import include, path
from posts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('authors/', views.get_authors, name='authors'),
    path('posts/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),

]
