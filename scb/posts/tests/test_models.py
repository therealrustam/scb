"""
Тесты модели приложения.
"""

from django.test import TestCase

from ..models import Author, Post


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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

    def test_models_have_correct_object_names(self):
        post = PostModelTest.post
        expected_object_name = post.title
        self.assertEqual(expected_object_name, str(post))
        authors = PostModelTest.authors
        expected_object_name = f'{authors.last_name} {authors.first_name}'
        self.assertEqual(expected_object_name, str(authors))
