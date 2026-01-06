from django.db.models import Q
from django.shortcuts import render, reverse
from django.views import generic

from customers.models import Customer

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
            customer = Customer.objects.get(id=customer_id)
            ids_list = [customer_id]
            if customer.friends.exists():
                ids_list = customer.friends.all().values_list('id', flat=True)
            qs = qs.filter(
                    Q(customer_id__in=ids_list)|
                    Q(receiver_id__in=ids_list)
                )
        return qs
    

class PaymentDetailView(generic.DetailView):
    model = Payment
    template_name = 'payments/detail.html'

    
