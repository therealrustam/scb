"""
Тесты формы создания и редактирования статьи.
"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Author, Post

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = 'auth'
        cls.user = User.objects.create_user(username=cls.username)
        cls.authors = Author.objects.create(
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович',
            date_of_birth='1990-12-14',
        )
        cls.post = Post.objects.create(
            title='Тест',
            text='Тестовый текст',
        )
        cls.post.authors.add(cls.authors)
        cls.form = PostForm()

    def setUp(self):
        self.user = User.objects.get(username=self.username)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        post_count = Post.objects.count()
        post_title = 'Новый заголовок'
        post_text = 'Новый текст'
        form_data = {
            'text': post_text,
            'title': post_title,
            'authors': self.authors.id,
        }
        response = self.authorized_client.post(
            reverse('create_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=post_text,
                title=post_title,
            ).exists()
        )

    def test_edit_post(self):
        post_text = 'Новый улучшенный текст'
        post_title = 'Новый улучшенный заголовок'
        form_data = {
            'text': post_text,
            'title': post_title,
            'authors': self.authors.id,
        }
        response = self.authorized_client.post(
            reverse('edit_post', args=[self.post.id]),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse(
            'index'))
        self.assertTrue(
            Post.objects.filter(
                text=post_text,
                id=self.post.id,
            ).exists()
        )
