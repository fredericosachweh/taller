from django.urls import path

from . import views

urlpatterns = [
    path(r'create/', views.CustomerCreateView.as_view(), name='create'),
]