from django.db import models
from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _

from customers.models import CreditCard, Customer


class StatusChoice(models.TextChoices):
    Accept = 'A', _('Accept')
    Declined = 'D', _('Declined')
    Refund = 'R', ('Refund')

class PaymentMethodChoice(models.TextChoices):
    Wallet = 'W', _('Wallet')
    Card = 'C', _('Credit Card')


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, null=True, blank=True)
    value = models.DecimalField(decimal_places=2, max_digits=100)
    status = models.CharField(choices=StatusChoice.choices, max_length=1, default=StatusChoice.Accept)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(choices=PaymentMethodChoice.choices, max_length=1, default=PaymentMethodChoice.Wallet)
    receiver = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='receiver')
    class Meta:
        verbose_name = _('Payment')


@receiver(models.signals.post_save, sender=Payment)
def update_balance(sender, instance, created, **kwargs):
    if created and instance.payment_method == 'W':
        wallet = instance.customer.wallet
        wallet.balance -= instance.value
        wallet.save()

@receiver(models.signals.post_save, sender=Payment)
def create_log(sender, instance, created, **kwargs):
    instance.paymentlog_set.create(
        status=instance.status
    )


class PaymentLog(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    processed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=StatusChoice.choices, max_length=1)

    class Meta:
        unique_together = ('payment', 'status')
