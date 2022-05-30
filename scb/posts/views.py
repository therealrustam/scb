from django.shortcuts import render

from .models import Author, Post

def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'home.html', context)
