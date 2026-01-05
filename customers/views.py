from django.shortcuts import render
from django.views import generic
# Create your views here.

from .forms import CustomerModelForm
from .models import Customer


class CustomerCreateView(generic.CreateView):
    model = Customer
    template_name = 'customers/create.html'
    form = CustomerModelForm