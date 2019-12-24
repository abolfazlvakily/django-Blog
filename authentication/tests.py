from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from article.models import Person, Article


class LoginLogoutSetUp(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='a_vakily', password='123')
        self.person = Person.objects.create(
            user_id=self.user,
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


class Login(LoginLogoutSetUp):
    def test_get(self):
        resp = self.client.get(reverse('authentication:login'))
        self.assertEqual(resp.status_code, 200)

    def test_post_form_valid(self):
        form = AuthenticationForm(data={'username': 'a_vakily', 'password': '123'})
        self.assertTrue(form.is_valid())

    def test_post_form_invalid(self):
        form = AuthenticationForm(data={'username': 'a_vakily', 'password': '12'})
        self.assertFalse(form.is_valid())

    def test_post_auth(self):
        form = AuthenticationForm(data={'username': 'a_vakily', 'password': '123'})
        self.assertTrue(form.is_valid())
        resp = self.client.post(reverse('authentication:login'), {'username': 'a_vakily', 'password': '123'})
        self.assertEqual(resp.status_code, 302)


class LogoutViewTests(LoginLogoutSetUp):
    def test_get_auth(self):
        self.client.login(username=self.user.username, password='123')
        resp = self.client.get(reverse('authentication:logout'))
        self.assertEqual(resp.status_code, 302)

    def test_get(self):
        resp = self.client.get(reverse('authentication:logout'))
        self.assertEqual(resp.status_code, 302)
