from django.test import TestCase
from django.urls import reverse

from .models import User


class AccountViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='student', password='test-password', role='student'
        )

    def test_logout_requires_post(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_logout_post_redirects_to_login(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('login'))
