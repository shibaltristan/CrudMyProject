from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import FarmerRegistration


class FarmerRegistrationTests(TestCase):
    def test_register_creates_user_and_profile(self):
        response = self.client.post(reverse('registration:register'), {
            'farmers_id': 'FARM-001',
            'first_name': 'Juan',
            'last_name': 'Dela Cruz',
            'middle_name': 'Santos',
            'mobile_number': '09171234567',
            'password': 'secure-test-password-123',
            'confirm_password': 'secure-test-password-123',
        })

        self.assertRedirects(response, reverse('record_list'))
        self.assertTrue(User.objects.filter(username='FARM-001').exists())
        profile = FarmerRegistration.objects.get(farmers_id='FARM-001')
        self.assertEqual(profile.mobile_number, '09171234567')

    def test_passwords_must_match(self):
        response = self.client.post(reverse('registration:register'), {
            'farmers_id': 'FARM-002',
            'first_name': 'Maria',
            'last_name': 'Reyes',
            'middle_name': '',
            'mobile_number': '09991234567',
            'password': 'secure-test-password-456',
            'confirm_password': 'different-password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords do not match.')
        self.assertFalse(User.objects.filter(username='FARM-002').exists())
