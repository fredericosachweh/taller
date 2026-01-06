from django.urls import path

from . import views

urlpatterns = [
    path(r'create/', views.CustomerCreateView.as_view(), name='create'),
    path(r'friends/<pk>/', views.CustomerFriendsView.as_view(), name='friends'),
]