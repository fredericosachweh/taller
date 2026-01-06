from django.shortcuts import render, reverse
from django.views import generic
# Create your views here.

from .forms import CustomerModelForm, CustomerFriendsModelForm
from .models import Customer


# Create Customers
class CustomerCreateView(generic.CreateView):
    model = Customer
    template_name = 'customers/create.html'
    form_class = CustomerModelForm
    
    def form_valid(self, form):
        customer = form.save(commit=False)
        password = customer.password
        customer.save()
        customer.set_password(password)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("customers:create")
    

class CustomerFriendsView(generic.UpdateView):
    model = Customer
    template_name = 'customers/friends.html'
    form_class = CustomerFriendsModelForm
    
    def get_success_url(self):
        return reverse("customers:friends", kwargs={'pk': self.kwargs['pk']})
