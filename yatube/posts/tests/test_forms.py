from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Post, Group
from django.urls import reverse


User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='admin')
        cls.authorized_client = Client()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый текст',
        )

    def setUp(self):
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post и происходит редирект"""
        form_data = {
            'text': 'Тестовый тескт_1',
            'group': self.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse('posts:profile', args=['admin'])
        )
        self.assertTrue(Post.objects.filter(
            text=form_data['text'], group=form_data['group']).exists())

    def test_edit_post(self):
        """Происходит изменение поста"""
        post_id = self.post.pk
        expected_text = 'Изменённый текст'
        form_data = {
            'text': expected_text,
            'group': self.group.pk,
        }
        self.authorized_client.post(
            reverse('posts:post_edit', args=(str(post_id))),
            data=form_data,
            follow=True
        )
        self.assertTrue(Post.objects.filter(
            text=form_data['text'], group=form_data['group']).exists())
