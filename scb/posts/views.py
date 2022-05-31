"""
Основные методы страниц приложения.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Author, Post


def index(request):
    """
    Метод главной страницы, где представлены
    последние добавленные статьи.
    """
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'index.html', context)


def get_authors(request):
    """
    Метод получения списка авторов.
    """
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


@login_required
def create_post(request):
    """
    Метод страницы создания статьи.
    """
    form = PostForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form_for_save = form.save(commit=False)
            form_for_save.save()
            return redirect('/')
        return render(request, 'create_post.html', {
            'form': form,
        })
    return render(request, 'create_post.html', {
        'form': form,
    })


@login_required
def edit_post(request, post_id):
    """
    Метод страницы редактирования статьи.
    """
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    form = PostForm(request.POST or None,
                    instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'create_post.html', {
        'form': form,
        'is_edit': is_edit,
    })
