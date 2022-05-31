"""
Тесты основных методов приложения.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Author, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = 'auth'
        cls.user = User.objects.create_user(username=cls.username)
        cls.title = 'Тестовая заголовок'
        cls.text = 'Тестовый текст'
        cls.authors = Author.objects.create(
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович',
            date_of_birth='1990-12-14',
        )
        cls.post = Post.objects.create(
            title=cls.title,
            text=cls.text,
        )
        cls.post.authors.add(cls.authors)
        cls.post_sum = 1

    def setUp(self):
        self.user = User.objects.get(username=self.username)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def assert_equal_method(self, assert_dictionary):
        self.assert_dictionary = assert_dictionary
        for name, value in self.assert_dictionary.items():
            with self.subTest(name=name):
                self.assertEqual(name, value)

    def test_pages_uses_correct_template(self):
        template_edit = 'create_post.html'
        template_create = 'create_post.html'
        templates_pages_names = {
            'index.html': reverse('index'),
            'authors.html': reverse('authors'),
            template_edit: reverse('edit_post', args=[self.post.id]),
            template_create: reverse('create_post'),
        }

        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('index'))
        first_object = response.context['posts'][0]
        post_text_0 = first_object.text
        post_title_0 = first_object.title
        assert_dictionary = {
            post_text_0: self.text,
            post_title_0: self.title,
        }
        self.assert_equal_method(assert_dictionary)

    def test_create_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('create_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'title': forms.fields.CharField,
            'authors': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
