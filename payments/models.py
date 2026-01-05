from django.db import models
from django.utils.translation import gettext_lazy as _

from customers.models import CreditCard, Customer


STATUS = (('A', _('Accept')), 'D', _('Declined'))


class Payment(models.Model):
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=2)
    status = models.CharField(choices=STATUS, max_length=1)
    paid_at = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(Customer, on_delete=models.CASCADE)


    class Meta:
        verbose_name = _('Payment')


class PaymentLog(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    processed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length=1)
