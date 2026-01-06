from django import forms

from customers.models import Wallet, CreditCard

from .models import Payment, PaymentMethodChoice


class PaymentModelForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['customer', 'receiver', 'value', 'credit_card', 'payment_method', 'description']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_method'].disabled = True 
        self.fields['credit_card'].disabled = True 


    def clean(self):
        data = super().clean()
        customer = data.get('customer')
        value = data.get('value')
        try:
            wallet = Wallet.objects.get(customer=customer)
        except Wallet.DoesNotExist:
            raise forms.ValidationError('Wallet does not exist.')
        if wallet.balance < value:
            try:
                credit_card = CreditCard.objects.get(default=True, customer=customer)
                data['credit_card'] = credit_card
                data['payment_method'] = PaymentMethodChoice.Card
            except CreditCard.DoesNotExist:
                raise forms.ValidationError('Credit Card does not exist.')
        return data