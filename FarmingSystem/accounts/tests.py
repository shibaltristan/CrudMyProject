from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class FarmerAccountTests(TestCase):
    def test_login_uses_farmers_id(self):
        User.objects.create_user(
            username='FARM-002',
            password='secure-test-password-456',
        )

        response = self.client.post(reverse('accounts:login'), {
            'username': 'FARM-002',
            'password': 'secure-test-password-456',
        })

        self.assertRedirects(response, reverse('record_list'))
