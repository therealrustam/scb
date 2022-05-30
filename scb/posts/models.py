from django.db import models


class Author(models.Model):
    """
    Создание модели автора.
    """
    first_name = models.CharField(max_length=150,
                                  verbose_name='Имя',
                                  help_text='Введите имя автора')
    last_name = models.CharField(max_length=150,
                                 verbose_name='Фамилия',
                                 help_text='Введите фамилию автора')
    patronymic = models.CharField(max_length=150,
                                  verbose_name='Отчество',
                                  help_text='Введите отчество автора')
    date_of_birth = models.DateField(verbose_name='Дата рождения',
                                     help_text='Введите дату рождения автора')

    class Meta:
        """
        Мета параметры модели.
        """
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def get_full_name(self):
        """"
        Метод получения полного имени авторов.
        """
        return f'{self.last_name} {self.first_name} {self.patronymic}'


class Post(models.Model):
    """
    Создание модели статьи.
    """
    title = models.CharField(max_length=150,
                             verbose_name='Заголовок статьи',
                             help_text='Введите заголовок статьи')
    text = models.TextField(verbose_name='Текст статьи',
                            help_text='Введите текст статьи')
    authors = models.ManyToManyField(Author,
                                     through='AuthorsPosts',
                                     related_name='posts')

    class Meta:
        """
        Мета параметры модели.
        """
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        """"
        Метод строкового представления модели.
        """
        return self.title


class AuthorsPosts(models.Model):
    posts = models.ForeignKey(Post,
                              related_name='authorsposts',
                              on_delete=models.CASCADE)
    authors = models.ForeignKey(Author,
                                related_name='authorsposts',
                                on_delete=models.CASCADE)

    class Meta:
        """
        Мета параметры модели.
        """
        verbose_name = 'Автор статьи'
        verbose_name_plural = 'Авторы статьи'

    def __str__(self):
        """"
        Метод строкового представления модели.
        """
        return f'{self.posts} {self.authors}'
