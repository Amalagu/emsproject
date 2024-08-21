from django import forms
from .models import CryptoTransaction, GiftCardTransaction,  Customer, BankAccount


class CryptoTransactionForm(forms.ModelForm):
    class Meta:
        model = CryptoTransaction
        fields = [
             'customer', 'transaction_type', 'coin_value', 'coin_quantity',
            'rate', 'coin_type', 'bonus', 'accounts_paid_into', 'settled_amount', 'settled', 'comments'
        ]
        widgets = {
            'timestamp': forms.DateTimeInput(attrs={
                'class': 'form-control', 'placeholder': 'Timestamp'
            }),
            'customer': forms.Select(attrs={
                'class': 'form-select', 'aria-label': 'Customer', 'id' :"crypto-customer"
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-select', 'aria-label': 'Transaction Type'
            }),
            'coin_value': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Coin Value in USD'
            }),
            'coin_quantity': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Coin Quantity'
            }),
            'rate': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Exchange Rate USD to NGN'
            }),
            'coin_type': forms.Select(attrs={
                'class': 'form-select', 'aria-label': 'Coin Type'
            }),
            'bonus': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Bonus in NGN'
            }),
            'accounts_paid_into': forms.SelectMultiple(attrs={
                'class': 'form-select', 'aria-label': 'Accounts Paid Into'
            }),
            'settled_amount': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Settled Amount in NGN'
            }),
            'settled': forms.CheckboxInput(attrs={
                'class': 'form-check-input', 'id': 'flexCheckChecked1'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Leave a comment here', 'style': 'height: 150px;'
            }),
        }

class GiftCardTransactionForm(forms.ModelForm):
    class Meta:
        model = GiftCardTransaction
        fields = [
             'customer', 'transaction_type', 'card_value',
            'rate', 'card_type', 'card_country', 'bonus','settled_amount', 'accounts_paid_into', 'settled', 'comments'
        ]
        widgets = {
            'timestamp': forms.DateTimeInput(attrs={
                'class': 'form-control', 'placeholder': 'Timestamp'
            }),
            'customer': forms.Select(attrs={
                'class': 'form-select', 'aria-label': 'Customer', 'id' :"giftcard-customer"
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-select', 'aria-label': 'Transaction Type'
            }),
            'card_value': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Card Value in USD'
            }),
            'rate': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Exchange Rate USD to NGN'
            }),
            'card_type': forms.Select(attrs={
                'class': 'form-select', 'aria-label': 'Card Type'
            }),
            'card_country': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Card Country'
            }),
            'bonus': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Bonus in NGN'
            }),
            'accounts_paid_into': forms.SelectMultiple(attrs={
                'class': 'form-select', 'aria-label': 'Accounts Paid Into'
            }),
            'settled_amount': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Settled Amount in NGN'
            }),
            'settled': forms.CheckboxInput(attrs={
                'class': 'form-check-input', 'id': 'flexCheckChecked2'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Leave a comment here', 'style': 'height: 150px;'
            }),
        }






class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'surname', 
            'othernames', 
            'gender', 
            'mobile_number', 
            'phone_number', 
            'address', 'dob',
            #joined_date
            ]

        widgets = {
            #'joined_date': forms.DateInput(attrs={'type': 'date'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['bank_name', 'account_number', 'account_type']



































""" from django import forms
from .models import CryptoTransaction, GiftCardTransaction

class CryptoTransactionForm(forms.ModelForm):
    class Meta:
        model = CryptoTransaction
        fields = '__all__'
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'coin_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'coin_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'coin_type': forms.TextInput(attrs={'class': 'form-control'}),
            'bonus': forms.NumberInput(attrs={'class': 'form-control'}),
            'account_paid_into': forms.TextInput(attrs={'class': 'form-control'}),
            'settled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class GiftCardTransactionForm(forms.ModelForm):
    class Meta:
        model = GiftCardTransaction
        fields = '__all__'
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'card_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'card_type': forms.TextInput(attrs={'class': 'form-control'}),
            'card_country': forms.TextInput(attrs={'class': 'form-control'}),
            'bonus': forms.NumberInput(attrs={'class': 'form-control'}),
            'accounts_paid_into': forms.TextInput(attrs={'class': 'form-control'}),
            'settled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
 """