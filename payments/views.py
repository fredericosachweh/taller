from django.shortcuts import render, reverse
from django.views import generic

from .forms import PaymentModelForm
from .models import Payment



class PaymentCreateView(generic.CreateView):
    model = Payment
    template_name = 'payments/create.html'
    form_class = PaymentModelForm

    def get_success_url(self):
        return reverse("customers:create")
    
