from django.contrib import admin

from .models import Author, AuthorsPosts, Post


class AuthorsPostsInline(admin.TabularInline):
    """
    Параметры настроек админ зоны
    модели авторов статьи.
    """
    model = AuthorsPosts
    extra = 0


class AuthorAdmin(admin.ModelAdmin):
    """
    Параметры админ зоны авторов.
    """
    list_display = ('first_name', 'last_name', 'patronymic', 'date_of_birth')
    search_fields = ('first_name', )
    empty_value_display = '-пусто-'
    list_filter = ('first_name',)


class PostAdmin(admin.ModelAdmin):
    """
    Параметры админ зоны статей.
    """
    inlines = (AuthorsPostsInline,)
    list_display = ('title', 'text')
    search_fields = ('title', )
    empty_value_display = '-пусто-'
    list_filter = ('title',)


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
