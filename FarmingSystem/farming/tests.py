from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import FarmingRecord


class FarmingRecordCrudTests(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(username='farmer-a', password='test-password-a')
        self.user_b = User.objects.create_user(username='farmer-b', password='test-password-b')
        self.client.force_login(self.user_a)
        self.record = FarmingRecord.objects.create(
            user=self.user_a,
            title='Seeds',
            record_type='Expense',
            amount=Decimal('500.00'),
            description='Seed purchase',
            date='2026-11-05',
        )

    def test_list_calculates_totals(self):
        FarmingRecord.objects.create(
            user=self.user_a,
            title='Harvest Sales',
            record_type='Income',
            amount=Decimal('5000.00'),
            description='',
            date='2026-11-06',
        )

        response = self.client.get(reverse('record_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['expenses'], Decimal('500.00'))
        self.assertEqual(response.context['income'], Decimal('5000.00'))
        self.assertEqual(response.context['profit'], Decimal('4500.00'))

    def test_create_update_and_delete_record(self):
        create_response = self.client.post(reverse('record_create'), {
            'title': 'Fertilizer',
            'record_type': 'Expense',
            'amount': '1000.00',
            'description': 'Crop fertilizer',
            'date': '2026-11-05',
        })
        self.assertRedirects(create_response, reverse('record_list'))

        record = FarmingRecord.objects.get(title='Fertilizer')
        update_response = self.client.post(reverse('record_update', args=[record.pk]), {
            'title': 'Updated Fertilizer',
            'record_type': 'Expense',
            'amount': '1200.00',
            'description': 'Updated fertilizer purchase',
            'date': '2026-11-05',
        })
        self.assertRedirects(update_response, reverse('record_list'))

        record.refresh_from_db()
        self.assertEqual(record.title, 'Updated Fertilizer')
        self.assertEqual(record.amount, Decimal('1200.00'))

        delete_response = self.client.post(reverse('record_delete', args=[record.pk]))
        self.assertRedirects(delete_response, reverse('record_list'))
        self.assertFalse(FarmingRecord.objects.filter(pk=record.pk).exists())

    def test_crud_success_messages_and_delete_confirmation(self):
        create_response = self.client.post(reverse('record_create'), {
            'title': 'New Record',
            'record_type': 'Income',
            'amount': '250.00',
            'description': '',
            'date': '2026-11-05',
        }, follow=True)
        self.assertContains(create_response, 'Farming record added successfully.')
        self.assertContains(create_response, 'sweetalert2@11')
        refreshed_response = self.client.get(reverse('record_list'))
        self.assertNotContains(refreshed_response, 'Farming record added successfully.')

        record = FarmingRecord.objects.get(title='New Record')
        confirmation_response = self.client.get(reverse('record_delete', args=[record.pk]))
        self.assertContains(confirmation_response, 'data-confirm-delete')

        update_response = self.client.post(reverse('record_update', args=[record.pk]), {
            'title': 'Updated Record',
            'record_type': 'Income',
            'amount': '275.00',
            'description': '',
            'date': '2026-11-05',
        }, follow=True)
        self.assertContains(update_response, 'Farming record updated successfully.')

        delete_response = self.client.post(
            reverse('record_delete', args=[record.pk]),
            follow=True,
        )
        self.assertContains(delete_response, 'Farming record deleted successfully.')

    def test_invalid_record_form_shows_error_notification(self):
        response = self.client.post(reverse('record_create'), {
            'title': '',
            'record_type': 'Expense',
            'amount': '100.00',
            'description': '',
            'date': '2026-11-05',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The record could not be added.')
        self.assertContains(response, 'django-messages')

        update_response = self.client.post(
            reverse('record_update', args=[self.record.pk]),
            {
                'title': '',
                'record_type': 'Expense',
                'amount': '100.00',
                'description': '',
                'date': '2026-11-05',
            },
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertContains(update_response, 'The record could not be updated.')

    def test_records_are_isolated_between_two_users(self):
        user_b_record = FarmingRecord.objects.create(
            user=self.user_b,
            title='User B Seeds',
            record_type='Expense',
            amount=Decimal('300.00'),
            description='Private to User B',
            date='2026-11-05',
        )

        response = self.client.get(reverse('record_list'))
        self.assertContains(response, 'Seeds')
        self.assertNotContains(response, 'User B Seeds')

        for url_name in ('record_update', 'record_delete'):
            response = self.client.get(reverse(url_name, args=[user_b_record.pk]))
            self.assertEqual(response.status_code, 404)
            response = self.client.post(reverse(url_name, args=[user_b_record.pk]), {
                'title': 'Leaked Update',
                'record_type': 'Expense',
                'amount': '999.00',
                'description': 'Unauthorized',
                'date': '2026-11-05',
            })
            self.assertEqual(response.status_code, 404)

        user_b_record.refresh_from_db()
        self.assertEqual(user_b_record.title, 'User B Seeds')
        self.assertEqual(user_b_record.user, self.user_b)

        create_response = self.client.post(reverse('record_create'), {
            'title': 'User A Record',
            'record_type': 'Income',
            'amount': '700.00',
            'description': '',
            'date': '2026-11-05',
        })
        self.assertRedirects(create_response, reverse('record_list'))
        created = FarmingRecord.objects.get(title='User A Record')
        self.assertEqual(created.user, self.user_a)

        self.client.force_login(self.user_b)
        response = self.client.get(reverse('record_list'))
        self.assertContains(response, 'User B Seeds')
        self.assertNotContains(response, '<strong>Seeds</strong>', html=True)
        self.assertNotContains(response, 'User A Record')
