from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Customer(AbstractUser):
    document = models.CharField(max_length=13)

    groups =  models.ManyToManyField(
        'auth.Group',
        related_name='customer_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='custom_user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

    class Meta:
        verbose_name = _('Customer')



"""class Wallet(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, verbose_name=_('Balance'))
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Wallet')


class CreditCard(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'))
    number = models.BigIntegerField(verbose_name=_('Number'))
    expire_date = models.DateField(verbose_name=_('Expire Date'))
    cvv = models.IntegerField(verbose_name=_('CVV'))
    credit = models.DecimalField(decimal_places=2, verbose_name=_('Credit'))
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Credit Card')"""


