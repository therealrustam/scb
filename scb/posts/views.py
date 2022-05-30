from django.shortcuts import render

from .models import Author, Post


def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'home.html', context)


def get_authors(request):
    queryset = Author.objects.prefetch_related('posts')
    authors = []
    sum_posts = []
    for author in queryset:
        post = Post.objects.filter(authors=author).count()
        sum_posts.append(post)
        authors.append(author)
    context = {
        'authors': authors,
        'sum_posts': sum_posts,
    }
    return render(request, 'authors.html', context)
