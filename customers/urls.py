from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.CustomerCreateView.as_view(), name='create'),
]