from django.contrib import admin

from .forms import PaymentModelForm
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    form = PaymentModelForm

admin.site.register(Payment, PaymentAdmin)