from django.test import TestCase, Client
from django.urls import reverse

from .models import Customer

class CustomerTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_create_user(self):
        data = {
            'username': 'test1',
            'email': 'test1@test.com',
            'first_name': 'test1',
            'last_name': 'last_test1',
            'document': 1223434,
            'password': '1234',
            'confirm_password': '1234',
        }

        response = self.client.post(reverse('customers:create'), data=data)
        self.assertEqual(response.status_code, 302)
        customer = Customer.objects.get()
        self.assertEqual(customer.username, data['username'])

    def test_create_user_with_wrong_password(self):
        data = {
            'username': 'test1',
            'email': 'test1@test.com',
            'first_name': 'test1',
            'last_name': 'last_test1',
            'document': 1223434,
            'password': '1234',
            'confirm_password': '123434',
        }

        response = self.client.post(reverse('customers:create'), data=data)
        self.assertEqual(response.status_code, 200)
        customer_count = Customer.objects.count()
        self.assertEqual(customer_count, 0)


