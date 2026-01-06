import random
from datetime import datetime, timedelta
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
    friends = models.ManyToManyField('Customer', blank=True)

    class Meta:
        verbose_name = _('Customer')

    def __str__(self):
        return self.first_name
    

@receiver(models.signals.post_save, sender=Customer)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(customer=instance)


class Wallet(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, max_digits=100, verbose_name=_('Balance'), default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Wallet')
    
    def __str__(self):
        return self.customer.first_name

class CreditCard(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'))
    number = models.BigIntegerField(verbose_name=_('Number'))
    expire_date = models.DateField(verbose_name=_('Expire Date'))
    cvv = models.IntegerField(verbose_name=_('CVV'))
    default = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Credit Card')

@receiver(models.signals.pre_save, sender=CreditCard)
def create_credit_card(sender, instance, **kwargs):
    if not instance.cvv:
        instance.cvv = random.randint(100, 999)
    if not instance.expire_date:
        instance.expire_date = (datetime.now() + timedelta(days=365)).date()


@receiver(models.signals.pre_save, sender=CreditCard)
def set_default_card(sender, instance, **kwargs):
    if instance.default:
        cards = CreditCard.objects.filter(customer=instance.customer)
        if instance.pk:
            cards = cards.exclude(id=instance.id)
        cards.update(default=False)

