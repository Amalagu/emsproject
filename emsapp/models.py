from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db.models import Sum, Q
from datetime import datetime, timedelta






########## USER ACCOUNTS #################################
class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name, last_name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email



########### CUSTOMER DETAILS TABLE ##############################

class Customer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    surname = models.CharField(max_length=100)
    othernames = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    mobile_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    joined_date = models.DateTimeField(default=timezone.now)
    address = models.TextField()
    dob = models.DateField(blank=True, null=True)

    def crypto_traded_today(self):
        today = datetime.now().date()
        return CryptoTransaction.objects.filter(customer=self, timestamp__date=today).aggregate(Sum('total_amount_paid'))['total_amount_paid__sum'] or 0

    def crypto_traded_this_month(self):
        today = datetime.now().date()
        first_day_of_month = today.replace(day=1)
        return CryptoTransaction.objects.filter(customer=self, timestamp__date__gte=first_day_of_month).aggregate(Sum('total_amount_paid'))['total_amount_paid__sum'] or 0

    def crypto_traded_this_year(self):
        today = datetime.now().date()
        first_day_of_year = today.replace(month=1, day=1)
        return CryptoTransaction.objects.filter(customer=self, timestamp__date__gte=first_day_of_year).aggregate(Sum('total_amount_paid'))['total_amount_paid__sum'] or 0

    def giftcard_traded_today(self):
        today = datetime.now().date()
        return GiftCardTransaction.objects.filter(customer=self, timestamp__date=today).aggregate(Sum('total_amount_paid'))['total_amount_paid__sum'] or 0

    def giftcard_traded_this_month(self):
        today = datetime.now().date()
        first_day_of_month = today.replace(day=1)
        return GiftCardTransaction.objects.filter(customer=self, timestamp__date__gte=first_day_of_month).aggregate(Sum('total_amount_paid'))['total_amount_paid__sum'] or 0

    def giftcard_traded_this_year(self):
        today = datetime.now().date()
        first_day_of_year = today.replace(month=1, day=1)
        return GiftCardTransaction.objects.filter(customer=self, timestamp__date__gte=first_day_of_year).aggregate(Sum('total_amount_paid'))['total_amount_paid__sum'] or 0

    def total_assets_traded_today(self):
        return self.crypto_traded_today() + self.giftcard_traded_today()

    def total_assets_traded_this_month(self):
        return self.crypto_traded_this_month() + self.giftcard_traded_this_month()

    def total_assets_traded_this_year(self):
        return self.crypto_traded_this_year() + self.giftcard_traded_this_year()

    def __str__(self):
        return f"{self.surname} {self.othernames}"

class BankAccount(models.Model):
    customer = models.ForeignKey(Customer, related_name='bank_accounts', on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    account_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"
    








################### TRANSACTION TABLES ####################################

class CryptoTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
        ('SWAP', 'Swap'),
    ]

    COIN_TYPES = [
        ('BTC', 'Bitcoin'),
        ('LTC', 'Litecoin'),
        ('ETH', 'Ethereum'),
        # Add other cryptocurrencies as needed
    ]

    timestamp = models.DateTimeField( auto_now_add= True)
    modified = models.DateTimeField( auto_now=True)
    customer = models.ForeignKey(Customer, to_field='phone_number', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    coin_value = models.DecimalField(max_digits=10, decimal_places=2)  # in USD
    coin_quantity = models.DecimalField(max_digits=20, decimal_places=10)  # number or fraction of the cryptocurrency
    rate = models.DecimalField(max_digits=10, decimal_places=2)  # exchange rate USD to NGN
    coin_type = models.CharField(max_length=3, choices=COIN_TYPES)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # in NGN
    #account_paid_into = models.ManyToManyField(BankAccount, blank=True)
    accounts_paid_into = models.ManyToManyField(BankAccount, blank=True)
    settled = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # calculated field
    total_amount_paid = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # calculated field
    settled_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # amount that has been paid
    deferred_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # amount deferred for later
    comments = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.amount = self.coin_value * self.rate
        self.total_amount_paid = self.amount + self.bonus
        self.deferred_amount = self.total_amount_paid - self.settled_amount
        super().save(*args, **kwargs)

    def settle_payment(self, amount):
        if amount <= self.total_amount_paid - self.settled_amount:
            self.settled_amount += amount
            self.deferred_amount = self.total_amount_paid - self.settled_amount
            if self.deferred_amount == 0:
                self.settled = True
            self.save()
        else:
            raise ValueError("Amount to settle exceeds the remaining balance.")

    """ @property
    def amount(self):
        return self.coin_value * self.rate

    @property
    def total_amount_paid(self):
        return self.amount + self.bonus """

    def __str__(self):
        return f"{self.customer.phone_number} - {self.coin_type} - {self.transaction_type}"
    



class GiftCardTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]

    CARD_TYPES = [
        ('VISAPAY', 'VisaPay'),
        ('RAZZERGOLD', 'RazzerGold'),
        ('ITUNES', 'iTunes Card'),
        # Add other gift cards as needed
    ]

    timestamp = models.DateTimeField( auto_now_add= True)
    modified = models.DateTimeField( auto_now=True)
    customer = models.ForeignKey(Customer, to_field='phone_number', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    card_value = models.DecimalField(max_digits=10, decimal_places=2)  # in USD
    rate = models.DecimalField(max_digits=10, decimal_places=2)  # exchange rate USD to NGN
    card_type = models.CharField(max_length=10, choices=CARD_TYPES)
    card_country = models.CharField(max_length=25, null=True, blank=True)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # in NGN
    accounts_paid_into = models.ManyToManyField(BankAccount, blank=True)
    settled = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # calculated field
    total_amount_paid = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # calculated field
    settled_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # amount that has been paid
    deferred_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # amount deferred for later
    comments = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.amount = self.card_value * self.rate
        self.total_amount_paid = self.amount + self.bonus
        self.deferred_amount = self.total_amount_paid - self.settled_amount
        super().save(*args, **kwargs)

    def settle_payment(self, amount):
        if amount <= self.total_amount_paid - self.settled_amount:
            self.settled_amount += amount
            self.deferred_amount = self.total_amount_paid - self.settled_amount
            if self.deferred_amount == 0:
                self.settled = True
            self.save()
        else:
            raise ValueError("Amount to settle exceeds the remaining balance.")

    """ @property
    def amount(self):
        return self.card_value * self.rate

    @property
    def total_amount_paid(self):
        return self.amount + self.bonus """

    def __str__(self):
        return f"{self.customer.phone_number} - {self.card_type} - {self.transaction_type}"


