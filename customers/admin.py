from django.contrib import admin

from .forms import CustomerModelForm
from .models import Customer, Wallet, CreditCard


class CustomerAdmin(admin.ModelAdmin):
    form = CustomerModelForm

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Wallet)
admin.site.register(CreditCard)
