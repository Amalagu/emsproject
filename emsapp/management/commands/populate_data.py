# myapp/management/commands/populate_data.py

import random
from django.core.management.base import BaseCommand
from faker import Faker
from emsapp.models import Customer, BankAccount, CryptoTransaction, GiftCardTransaction

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Create customers
        for _ in range(10):  # Adjust the range to create more or fewer customers
            customer = Customer.objects.create(
                surname=fake.last_name(),
                othernames=fake.first_name(),
                gender=random.choice(['M', 'F', 'O']),
                mobile_number=fake.unique.phone_number(),
                phone_number=fake.unique.phone_number(),
                address=fake.address(),
            )
            
            # Create bank accounts for each customer
            for _ in range(random.randint(1, 3)):  # Each customer can have 1 to 3 bank accounts
                BankAccount.objects.create(
                    customer=customer,
                    bank_name=fake.company(),
                    account_number=fake.unique.bban(),
                    account_type=random.choice(['Savings', 'Checking']),
                )
            
            # Create crypto transactions for each customer
            for _ in range(random.randint(1, 5)):  # Each customer can have 1 to 5 crypto transactions
                coin_value = random.uniform(100, 10000)  # in USD
                rate = random.uniform(500, 1000)  # exchange rate USD to NGN
                coin_quantity = random.uniform(0.01, 5)  # number or fraction of cryptocurrency
                CryptoTransaction.objects.create(
                    customer=customer,
                    transaction_type=random.choice(['BUY', 'SELL', 'SWAP']),
                    coin_value=coin_value,
                    coin_quantity=coin_quantity,
                    rate=rate,
                    coin_type=random.choice(['BTC', 'LTC', 'ETH']),
                    bonus=random.uniform(0, 5000),  # in NGN
                )
            
            # Create gift card transactions for each customer
            for _ in range(random.randint(1, 5)):  # Each customer can have 1 to 5 gift card transactions
                card_value = random.uniform(50, 500)  # in USD
                rate = random.uniform(500, 1000)  # exchange rate USD to NGN
                GiftCardTransaction.objects.create(
                    customer=customer,
                    transaction_type=random.choice(['BUY', 'SELL']),
                    card_value=card_value,
                    rate=rate,
                    card_type=random.choice(['VISAPAY', 'RAZZERGOLD', 'ITUNES']),
                    bonus=random.uniform(0, 1000),  # in NGN
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data'))


""" # myapp/management/commands/populate_data.py

import random
from django.core.management.base import BaseCommand
from faker import Faker
from emsapp.models import Customer, BankAccount, CryptoTransaction, GiftCardTransaction

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Create customers
        for _ in range(10):  # Adjust the range to create more or fewer customers
            customer = Customer.objects.create(
                surname=fake.last_name(),
                othernames=fake.first_name(),
                gender=random.choice(['M', 'F', 'O']),
                mobile_number=fake.unique.phone_number(),
                phone_number=fake.unique.phone_number(),
                address=fake.address(),
            )
            
            # Create bank accounts for each customer
            for _ in range(random.randint(1, 3)):  # Each customer can have 1 to 3 bank accounts
                BankAccount.objects.create(
                    customer=customer,
                    bank_name=fake.company(),
                    account_number=fake.unique.bban(),
                    account_type=random.choice(['Savings', 'Checking']),
                )
            
            # Create crypto transactions for each customer
            for _ in range(random.randint(1, 5)):  # Each customer can have 1 to 5 crypto transactions
                coin_value = random.uniform(100, 10000)  # in USD
                rate = random.uniform(500, 1000)  # exchange rate USD to NGN
                coin_quantity = random.uniform(0.01, 5)  # number or fraction of cryptocurrency
                CryptoTransaction.objects.create(
                    customer=customer,
                    transaction_type=random.choice(['BUY', 'SELL', 'SWAP']),
                    coin_value=coin_value,
                    coin_quantity=coin_quantity,
                    rate=rate,
                    coin_type=random.choice(['BTC', 'LTC', 'ETH']),
                    bonus=random.uniform(0, 5000),  # in NGN
                )
            
            # Create gift card transactions for each customer
            for _ in range(random.randint(1, 5)):  # Each customer can have 1 to 5 gift card transactions
                card_value = random.uniform(50, 500)  # in USD
                rate = random.uniform(500, 1000)  # exchange rate USD to NGN
                GiftCardTransaction.objects.create(
                    customer=customer,
                    transaction_type=random.choice(['BUY', 'SELL']),
                    card_value=card_value,
                    rate=rate,
                    card_type=random.choice(['VISAPAY', 'RAZZERGOLD', 'ITUNES']),
                    bonus=random.uniform(0, 1000),  # in NGN
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data'))
 """