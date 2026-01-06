from django.urls import path

from . import views

urlpatterns = [
    path(r'create/', views.PaymentCreateView.as_view(), name='create'),
    path(r'list/', views.PaymentListView.as_view(), name='list'),
    path(r'list/<customer_id>/', views.PaymentListView.as_view(), name='list'),
]