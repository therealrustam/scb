"""
Формы создания статей.
"""

from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """
    Форма создания статьи.
    """
    class Meta:
        model = Post
        fields = ('title', 'text', 'authors')
