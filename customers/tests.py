from datetime import datetime, timedelta
from django.test import TestCase, Client
from django.urls import reverse

from .models import Customer, Wallet, CreditCard

class CustomerTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.data1 = {
            'username': 'test1',
            'email': 'test1@test.com',
            'first_name': 'test1',
            'last_name': 'last_test1',
            'document': 1223434,
            'password': '1234',
        }

    def test_create_user(self):
        data = self.data1
        data['confirm_password'] = '1234'

        response = self.client.post(reverse('customers:create'), data=data)
        self.assertEqual(response.status_code, 302)
        customer = Customer.objects.get()
        self.assertEqual(customer.username, data['username'])

    def test_create_user_with_wrong_password(self):
        data = self.data1
        data['confirm_password'] = '212121'

        response = self.client.post(reverse('customers:create'), data=data)
        self.assertEqual(response.status_code, 200)
        customer_count = Customer.objects.count()
        self.assertEqual(customer_count, 0)


    def test_create_wallet(self):
        data = self.data1
        data['confirm_password'] = '1234'

        response = self.client.post(reverse('customers:create'), data=data)
        self.assertEqual(response.status_code, 302)
        wallet = Wallet.objects.get()
        self.assertEqual(wallet.customer.username, data['username'])


    def test_create_credit_card(self):
        data = self.data1
        customer = Customer.objects.create(**data)
        credit_card = CreditCard.objects.create(
            customer=customer,
            number=1234567890123456
        )
        self.assertEqual(credit_card.expire_date, (datetime.now() + timedelta(days=365)).date())
        self.assertTrue(credit_card.default)


    def test_create_credit_card_set_default(self):
        data = self.data1
        customer = Customer.objects.create(**data)
        credit_card = CreditCard.objects.create(
            customer=customer,
            number=1234567890123456
        )
        credit_card_2 = CreditCard.objects.create(
            customer=customer,
            number=1234567890123457
        )
        credit_card.refresh_from_db()
        self.assertFalse(credit_card.default)
        self.assertTrue(credit_card_2.default)
