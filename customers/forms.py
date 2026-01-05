from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Customer


class CustomerModelForm(forms.ModelForm):
    password = forms.CharField()
    confirm_password = forms.CharField()

    def clean(self):
        data = super().clean()
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            self.add_error('password', _('Password and confirm password not match.'))
        return data

    class Meta:
        model = Customer
        fields = ['username', 'email', 'first_name', 'last_name', 'document', 'password', 'confirm_password']

