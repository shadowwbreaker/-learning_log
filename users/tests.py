from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class RegistrationTests(TestCase):
    def test_registration_view(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_registration_form(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_view(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log in')

    def test_login_form(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

class LogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_logout_view(self):
        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have been logged out.')
        self.assertFalse('_auth_user_id' in self.client.session)

