from django.test import TestCase
from .models import Person, Article
from django.urls import reverse
from django.contrib.auth.models import User


class ArticleViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='a_vakily', password='123')
        self.person = Person.objects.create(
            first_name='abolfazl',
            last_name='vakily',
            phone_number='0915',
            address='My address',
        )
        self.article = Article.objects.create(
            person_id=self.person,
            title='what is test?!',
            content='hello world!',
        )

    def test_list(self):
        resp = self.client.get(reverse('article:article'))
        self.assertEqual(resp.status_code, 200)

    def test_detail(self):
        resp = self.client.get(reverse('article:detail', kwargs={'hash_id': self.article.hash_id}))
        self.assertEqual(resp.status_code, 200)

    def test_add(self):
        resp = self.client.post(reverse('article:article'))
        self.assertEqual(resp.status_code, 302)

    def test_add_auth(self):
        self.client.login(username=self.user.username, password='123')
        resp = self.client.post(reverse('article:article'))
        self.assertEqual(resp.status_code, 200)

    def test_delete(self):
        resp = self.client.delete(reverse('article:article'))
        self.assertEqual(resp.status_code, 302)

    def test_delete_auth(self):
        self.client.login(username=self.user.username, password='123')
        resp = self.client.delete(reverse('article:detail', kwargs={'hash_id': self.article.hash_id}))
        self.assertEqual(resp.status_code, 200)
