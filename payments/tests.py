from decimal import Decimal as D
from django.test import TestCase, Client
from django.urls import reverse

from customers.models import Customer, CreditCard

from .models import Payment, PaymentMethodChoice


class PaymentTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        customer_data1 = {
            'username': 'test1',
            'email': 'test1@test.com',
            'first_name': 'test1',
            'last_name': 'last_test1',
            'document': 1223434,
            'password': '1234',
        }
        self.customer1 = Customer.objects.create(**customer_data1)
        customer_data2 = {
            'username': 'test2',
            'email': 'test2@test.com',
            'first_name': 'test2',
            'last_name': 'last_test2',
            'document': 1223434,
            'password': '1234',
        }
        self.customer2 = Customer.objects.create(**customer_data2)


    def test_create_payment_wallet(self):
        wallet = self.customer1.wallet
        wallet.balance = D('1000.00')
        wallet.save()
        wallet.refresh_from_db()
        payment_data = {
            'customer': self.customer1.id,
            'receiver': self.customer2.id,
            'value': D('200.00')
        }
        response = self.client.post(reverse('payments:create'), data=payment_data)
        self.assertEqual(response.status_code, 302)
        wallet.refresh_from_db()
        self.assertEqual(wallet.balance, D('800.00'))
        payment = Payment.objects.get()
        self.assertEqual(payment.payment_method, PaymentMethodChoice.Wallet)


    def test_create_payment_credit_card(self):
        CreditCard.objects.create(
            customer=self.customer1,
            number=1234567890123456
        )
        wallet = self.customer1.wallet
        wallet.balance = D('1000.00')
        wallet.save()
        wallet.refresh_from_db()
        payment_data = {
            'customer': self.customer1.id,
            'receiver': self.customer2.id,
            'value': D('2000.00')
        }
        response = self.client.post(reverse('payments:create'), data=payment_data)
        self.assertEqual(response.status_code, 302)
        wallet.refresh_from_db()
        self.assertEqual(wallet.balance, D('1000.00'))
        payment = Payment.objects.get()
        self.assertEqual(payment.payment_method, PaymentMethodChoice.Card)

    def test_create_payment_error(self):
        wallet = self.customer1.wallet
        wallet.balance = D('1000.00')
        wallet.save()
        wallet.refresh_from_db()
        payment_data = {
            'customer': self.customer1.id,
            'receiver': self.customer2.id,
            'value': D('2000.00')
        }
        response = self.client.post(reverse('payments:create'), data=payment_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(wallet.balance, D('1000.00'))
        payments_count = Payment.objects.count()
        self.assertEqual(payments_count, 0)

    def test_list_payments(self):
        payment_data = {
            'customer': self.customer1,
            'receiver': self.customer2,
            'value': D('200.00')
        }
        Payment.objects.create(**payment_data)
        response = self.client.get(reverse('payments:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)

    def test_list_payments_by_user(self):
        customer_data3 = {
            'username': 'test3',
            'email': 'test3@test.com',
            'first_name': 'test3',
            'last_name': 'last_test3',
            'document': 1223434,
            'password': '1234',
        }
        customer3 = Customer.objects.create(**customer_data3)
        payment_data = {
            'customer': self.customer1,
            'receiver': self.customer2,
            'value': D('200.00')
        }
        Payment.objects.create(**payment_data)
        response = self.client.get(reverse('payments:list', kwargs={'customer_id': self.customer1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)
        response2 = self.client.get(reverse('payments:list', kwargs={'customer_id': self.customer2.id}))
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.context['object_list']), 1)
        response3 = self.client.get(reverse('payments:list', kwargs={'customer_id': customer3.id}))
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(len(response3.context['object_list']), 0)

    def test_payment_detail(self):
        payment_data = {
            'customer': self.customer1,
            'receiver': self.customer2,
            'value': D('200.00')
        }
        payment = Payment.objects.create(**payment_data)
        response = self.client.get(reverse('payments:detail', kwargs={'pk': payment.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].id, 1)

    def test_list_payments_by_user_and_friends(self):
        customer_data3 = {
            'username': 'test3',
            'email': 'test3@test.com',
            'first_name': 'test3',
            'last_name': 'last_test3',
            'document': 1223434,
            'password': '1234',
        }
        customer3 = Customer.objects.create(**customer_data3)
        payment_data = {
            'customer': self.customer1,
            'receiver': self.customer2,
            'value': D('200.00')
        }
        Payment.objects.create(**payment_data)
        response = self.client.get(reverse('payments:list', kwargs={'customer_id': self.customer1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)
        response2 = self.client.get(reverse('payments:list', kwargs={'customer_id': self.customer2.id}))
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.context['object_list']), 1)
        customer3.friends.add(self.customer1)
        response3 = self.client.get(reverse('payments:list', kwargs={'customer_id': customer3.id}))
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(len(response3.context['object_list']), 1)

