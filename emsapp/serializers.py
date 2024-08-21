from rest_framework import serializers
from .models import BankAccount, CryptoTransaction, GiftCardTransaction

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'




class CryptoTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoTransaction
        fields = '__all__'

class GiftCardTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCardTransaction
        fields = '__all__'
