from django.db.models import Q
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
    

class PaymentListView(generic.ListView):
    model = Payment
    template_name = 'payments/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        
        customer_id = self.kwargs.get('customer_id', None)
        if customer_id:
            qs = qs.filter(Q(customer_id=customer_id)|Q(receiver_id=customer_id))
        return qs
    

class PaymentDetailView(generic.DetailView):
    model = Payment
    template_name = 'payments/detail.html'

    
