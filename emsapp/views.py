
from django.shortcuts import render, redirect, get_object_or_404
from .models import CryptoTransaction, GiftCardTransaction, Customer, BankAccount
from .forms import CryptoTransactionForm, GiftCardTransactionForm, CustomerForm, BankAccountForm
from datetime import date, datetime
from django.db.models import Sum, Count, Q, Value, CharField
from decimal import Decimal
from django.forms import modelformset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

#REST  FRAMWORK IMPORTS
from rest_framework import generics
from .serializers import BankAccountSerializer




def home(request):
    # Fetch recent crypto transactions
    recent_crypto_transactions = CryptoTransaction.objects.all().order_by('-timestamp')[:5]

    # Fetch recent gift card transactions
    recent_giftcard_transactions = GiftCardTransaction.objects.all().order_by('-timestamp')[:5]

    # Combine and sort by date
    recent_transactions = list(recent_crypto_transactions) + list(recent_giftcard_transactions)
    recent_transactions.sort(key=lambda x: x.timestamp, reverse=True)

    # Prepare data for the template
    transactions_data = []
    for transaction in recent_transactions:
        invoice_number = f"INV-{transaction.id}"
        transaction_type = "Crypto" if isinstance(transaction, CryptoTransaction) else "GiftCard"
        customer_name = str(transaction.customer)  # Using the __str__ method of Customer model
        transactions_data.append({
            'date': transaction.timestamp,
            'id' : transaction.id,
            'invoice': invoice_number,
            'customer': customer_name,
            'amount': transaction.amount,
            'status': transaction.settled,
            'type': transaction_type,
        })

    # Get today's date
    today = date.today()

    # Calculate total sales for gift card today (using amount, excluding bonuses)
    giftcard_sales_today = GiftCardTransaction.objects.filter(
        timestamp__date=today
    ).aggregate(
        total_sales=Sum('amount'),
        total_transactions=Count('id')
    )

    # Calculate total sales for crypto today
    crypto_sales_today = CryptoTransaction.objects.filter(
        timestamp__date=today
    ).aggregate(
        total_sales=Sum('amount'),
        total_transactions=Count('id')
    )

    # Calculate collective total sales for both commodities
    collective_sales_today = (giftcard_sales_today['total_sales'] or 0) + (crypto_sales_today['total_sales'] or 0)

    # Calculate overall number of transactions carried out today
    total_transactions_today = giftcard_sales_today['total_transactions'] + crypto_sales_today['total_transactions']

    context = {
        'transactions': transactions_data,
        'giftcard_sales_today': giftcard_sales_today['total_sales'] or 0,
        'crypto_sales_today': crypto_sales_today['total_sales'] or 0,
        'collective_sales_today': collective_sales_today,
        'total_transactions_today': total_transactions_today,
    }

    return render(request, 'index.html', context)







# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .forms import CryptoTransactionForm, GiftCardTransactionForm
from .models import CryptoTransaction, GiftCardTransaction

def enter_transaction_view(request, transaction_type=None, transaction_id=None):
    if transaction_type == 'crypto':
        
        if transaction_id:
            transaction = get_object_or_404(CryptoTransaction, id=transaction_id)
            crypto_form = CryptoTransactionForm(instance=transaction)
        else:
            crypto_form = CryptoTransactionForm()
        giftcard_form = GiftCardTransactionForm()
    elif transaction_type == 'giftcard':
        if transaction_id:
            transaction = get_object_or_404(GiftCardTransaction, id=transaction_id)
            giftcard_form = GiftCardTransactionForm(instance=transaction)
        else:
            giftcard_form = GiftCardTransactionForm()
        crypto_form = CryptoTransactionForm()
    else:
        crypto_form = CryptoTransactionForm()
        giftcard_form = GiftCardTransactionForm()

    if request.method == 'POST':
        #print(request.POST)
        form_type = request.POST.get('form_type')
        if form_type == 'crypto_form':
            if transaction_id:
                crypto_form = CryptoTransactionForm(request.POST, instance=transaction)
            else:
                crypto_form = CryptoTransactionForm(request.POST)
            if crypto_form.is_valid():
                saved_transaction=crypto_form.save()
                #return redirect('home')  # Replace with your success URL or view
                return redirect('view_transaction_detail', transaction_type='crypto', transaction_id=saved_transaction.id)
        elif form_type == 'giftcard_form':
            if transaction_id:
                giftcard_form = GiftCardTransactionForm(request.POST, instance=transaction)
            else:
                giftcard_form = GiftCardTransactionForm(request.POST)
            if giftcard_form.is_valid():
                saved_transaction=giftcard_form.save()
                #return redirect('home')  # Replace with your success URL or view
                return redirect('view_transaction_detail', transaction_type='giftcard', transaction_id=saved_transaction.id)

    return render(request, 'transaction_form copy.html', {
        'crypto_form': crypto_form,
        'giftcard_form': giftcard_form,
        'transaction_type': transaction_type
    })



""" def add_edit_transaction_view(request, transaction_type, transaction_id=None):
    if transaction_type == 'crypto':
        if transaction_id:
            transaction = get_object_or_404(CryptoTransaction, id=transaction_id)
            crypto_form = CryptoTransactionForm(request.POST or None, instance=transaction)
        else:
            crypto_form = CryptoTransactionForm(request.POST or None)
        giftcard_form = GiftCardTransactionForm()

        if request.method == 'POST' and crypto_form.is_valid():
            crypto_form.save()
            return redirect('home')  # Replace with your success URL or view

    elif transaction_type == 'giftcard':
        if transaction_id:
            transaction = get_object_or_404(GiftCardTransaction, id=transaction_id)
            giftcard_form = GiftCardTransactionForm(request.POST or None, instance=transaction)
        else:
            giftcard_form = GiftCardTransactionForm(request.POST or None)
        crypto_form = CryptoTransactionForm()

        if request.method == 'POST' and giftcard_form.is_valid():
            giftcard_form.save()
            return redirect('home')  # Replace with your success URL or view

    return render(request, 'transaction_form.html', {
        'crypto_form': crypto_form,
        'giftcard_form': giftcard_form,
        'transaction_type': transaction_type
    })
 """

""" def add_edit_transaction_view(request, transaction_type, transaction_id=None):
    if transaction_type == 'crypto':
        if transaction_id:
            transaction = get_object_or_404(CryptoTransaction, id=transaction_id)
            crypto_form = CryptoTransactionForm(request.POST or None, instance=transaction)
        else:
            crypto_form = CryptoTransactionForm(request.POST or None)
        
        giftcard_form = GiftCardTransactionForm()

        if request.method == 'POST' and crypto_form.is_valid():
            crypto_form.save()
            return redirect('home')  # Replace with your success URL or view

    elif transaction_type == 'giftcard':
        if transaction_id:
            transaction = get_object_or_404(GiftCardTransaction, id=transaction_id)
            giftcard_form = GiftCardTransactionForm(request.POST or None, instance=transaction)
        else:
            giftcard_form = GiftCardTransactionForm(request.POST or None)
        
        crypto_form = CryptoTransactionForm()

        if request.method == 'POST' and giftcard_form.is_valid():
            giftcard_form.save()
            return redirect('home')  # Replace with your success URL or view
    
    return render(request, 'transaction_form.html', {
        'crypto_form': crypto_form,
        'giftcard_form': giftcard_form,
        'transaction_type': transaction_type
    }) """






#path('transaction_detail', views.view_transaction_detail, name='view_transaction_detail' ),
def view_transaction_detail(request, transaction_type=None, transaction_id = None):
    transaction_type = transaction_type if transaction_type else request.GET.get('type')
    transaction_id = transaction_id if transaction_id else request.GET.get('id')
    
    if transaction_type == 'crypto':
        transaction = get_object_or_404(CryptoTransaction, id=transaction_id)
    elif transaction_type == 'giftcard':
        transaction = get_object_or_404(GiftCardTransaction, id=transaction_id)
    else:
        # Handle the case where the type is not recognized
        transaction = None

    context = {
        'transaction': transaction,
        'transaction_type': transaction_type
    }
    
    return render(request, 'transaction_details.html', context)



def delete_transaction_view(request, transaction_type, transaction_id):
    if transaction_type == 'crypto':
        transaction = get_object_or_404(CryptoTransaction, id=transaction_id)
    elif transaction_type == 'giftcard':
        transaction = get_object_or_404(GiftCardTransaction, id=transaction_id)
    else:
        return redirect('home')  # or handle invalid transaction_type
    
    transaction.delete()
    return redirect('home')  # Replace with your success URL or view
    
   









def transactions_view(request):
    transactions = []
    transaction_type = request.GET.get('transaction_type', 'all')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    customer = request.GET.get('customer') if request.GET.get('customer') else ''
    status = request.GET.get('status')
    order_by = request.GET.get('order_by', 'timestamp')
    page = request.GET.get('page') if request.GET.get('page') else 1

    filters = Q()
    if date_from:
        filters &= Q(timestamp__gte=date_from)
    if date_to:
        filters &= Q(timestamp__lte=date_to)
    if customer:
        filters &= Q(customer__phone_number__icontains=customer)
    if status:
        filters &= Q(settled=status.lower() == 'true')

    print('THIS IS FILTER', filters)

    if transaction_type == 'crypto':
        transactions = CryptoTransaction.objects.filter(filters).order_by(order_by).annotate(commodity_type=Value('Crypto', output_field=CharField()))
        
    elif transaction_type == 'giftcard':
        transactions = GiftCardTransaction.objects.filter(filters).order_by(order_by).annotate(commodity_type=Value('Giftcard', output_field=CharField()))
        
    else:
        crypto_transactions = CryptoTransaction.objects.filter(filters).order_by(order_by).annotate(commodity_type=Value('Crypto', output_field=CharField()))
        giftcard_transactions = GiftCardTransaction.objects.filter(filters).order_by(order_by).annotate(commodity_type=Value('Giftcard', output_field=CharField()))
        transactions = list(crypto_transactions) + list(giftcard_transactions)
    


    #PAGINATION STARTS
    paginator = Paginator(transactions, 10)
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        page= 1
        transactions = paginator.page(page)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    startindex = int(page) - 3
    if startindex < 1: startindex = 1

    endindex = int(page) + 3
    if endindex > paginator.num_pages: endindex = paginator.num_pages + 1

    custom_range = range(startindex, endindex)

    #PAGINATION ENDS

    context = {
        'transactions': transactions,
        'transaction_type': transaction_type,
        'date_from': date_from,
        'date_to': date_to,
        'customer': customer,
        'status': status,
        'order_by': order_by,
        'paginator' : paginator,
        'custom_range': custom_range,
        'current_page' : transactions.number
    }
    return render(request, 'transactions.html', context)



################################################################
#            CUSTOMER SECTION
###################################################################


from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from datetime import datetime

def all_customers(request):
    surname = request.GET.get('surname', '')
    othernames = request.GET.get('othernames', '')
    gender = request.GET.get('gender', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    order_by = request.GET.get('order_by', 'surname')
    page = request.GET.get('page') if request.GET.get('page') else 1

    today = datetime.today()

    # Filter customers
    customers = Customer.objects.all()
    
    if surname:
        customers = customers.filter(surname__icontains=surname)
    if othernames:
        customers = customers.filter(othernames__icontains=othernames)
    if gender:
        customers = customers.filter(gender=gender)
    if date_from:
        customers = customers.filter(joined_date__gte=date_from)
    if date_to:
        customers = customers.filter(joined_date__lte=date_to)
    
    # Annotate customers with aggregated transaction data
    customers = customers.annotate(
        crypto_today=Sum('cryptotransaction__amount', filter=TruncDay('cryptotransaction__timestamp') == today),
        crypto_this_month=Sum('cryptotransaction__amount', filter=TruncMonth('cryptotransaction__timestamp') == today),
        crypto_this_year=Sum('cryptotransaction__amount', filter=TruncYear('cryptotransaction__timestamp') == today),
        giftcard_today=Sum('giftcardtransaction__amount', filter=TruncDay('giftcardtransaction__timestamp') == today),
        giftcard_this_month=Sum('giftcardtransaction__amount', filter=TruncMonth('giftcardtransaction__timestamp') == today),
        giftcard_this_year=Sum('giftcardtransaction__amount', filter=TruncYear('giftcardtransaction__timestamp') == today),
        assets_today=Sum('cryptotransaction__amount', filter=TruncDay('cryptotransaction__timestamp') == today) +
                     Sum('giftcardtransaction__amount', filter=TruncDay('giftcardtransaction__timestamp') == today),
        assets_this_month=Sum('cryptotransaction__amount', filter=TruncMonth('cryptotransaction__timestamp') == today) +
                          Sum('giftcardtransaction__amount', filter=TruncMonth('giftcardtransaction__timestamp') == today),
        assets_this_year=Sum('cryptotransaction__amount', filter=TruncYear('cryptotransaction__timestamp') == today) +
                         Sum('giftcardtransaction__amount', filter=TruncYear('giftcardtransaction__timestamp') == today),
    )
    
    # Order customers based on the selected criteria
    if order_by in ['crypto_today', 'crypto_this_month', 'crypto_this_year', 'giftcard_today', 
                    'giftcard_this_month', 'giftcard_this_year', 'assets_today', 'assets_this_month', 'assets_this_year']:
        customers = customers.order_by(f'-{order_by}')  # Descending order by default

    customers = customers.order_by(order_by) if order_by else customers.order_by('surname')

    #PAGINATION STARTS
    paginator = Paginator(customers, 5)
    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        page= 1
        customers = paginator.page(page)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    startindex = int(page) - 3
    if startindex < 1: startindex = 1

    endindex = int(page) + 3
    if endindex > paginator.num_pages: endindex = paginator.num_pages + 1

    custom_range = range(startindex, endindex)

    #PAGINATION ENDS

    context ={
        'customers': customers,
        'order_by': order_by,
        'custom_range': custom_range,
        'paginator': paginator,
        'current_page' : customers.number
        }

    return render(request, 'customers.html', context)





""" 
def all_customers(request):
    surname = request.GET.get('surname', '')
    othernames = request.GET.get('othernames', '')
    gender = request.GET.get('gender', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    order_by = request.GET.get('order_by', 'surname')

    customers = Customer.objects.all()

    if surname:
        customers = customers.filter(surname__icontains=surname)
    if othernames:
        customers = customers.filter(othernames__icontains(othernames))
    if gender:
        customers = customers.filter(gender=gender)
    if date_from:
        customers = customers.filter(joined_date__gte=date_from)
    if date_to:
        customers = customers.filter(joined_date__lte=date_to)

    customers = customers.order_by(order_by)

    return render(request, 'customers.html', {'customers': customers}) """








from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Customer, CryptoTransaction, GiftCardTransaction

def get_total_deferred_amount(customer):
    return CryptoTransaction.objects.filter(
        customer=customer, 
        settled=False
    ).aggregate(total_deferred=Sum('amount'))['total_deferred'] or 0.00

def get_total_amount_paid(customer):
    crypto_paid = CryptoTransaction.objects.filter(
        customer=customer, 
        settled=True
    ).aggregate(total_paid=Sum('amount'))['total_paid'] or Decimal(0.00)

    giftcard_paid = GiftCardTransaction.objects.filter(
        customer=customer, 
        settled=True
    ).aggregate(total_paid=Sum('amount'))['total_paid'] or Decimal(0.00)

    return crypto_paid + giftcard_paid

def view_customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    total_deferred_amount = get_total_deferred_amount(customer)
    total_amount_paid = get_total_amount_paid(customer)

    crypto_transactions = CryptoTransaction.objects.filter(customer=customer).annotate(commodity_type=Value('Crypto', output_field=CharField()))
    giftcard_transactions = GiftCardTransaction.objects.filter(customer=customer).annotate(commodity_type=Value('GiftCard', output_field=CharField()))

    transactions = list(crypto_transactions) + list(giftcard_transactions)

    context = {
        'customer': customer,
        'total_deferred_amount': total_deferred_amount,
        'total_amount_paid': total_amount_paid,
        'transactions': transactions
    }

    return render(request, 'customer_details.html', context)





def add_or_edit_customer(request, customer_id=None):
    if customer_id:
        customer = get_object_or_404(Customer, id=customer_id)
    else:
        customer = None

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            return redirect('view_customer_detail', customer_id=customer.id)
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customer_form.html', {'form': form})



def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')  # Update this to your customer list view
    #return render(request, 'delete_customer.html', {'customer': customer})




def add_account(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        bank_names = request.POST.getlist('bank_name')
        account_numbers = request.POST.getlist('account_number')
        account_types = request.POST.getlist('account_type')
 
        for bank_name, account_number, account_type in zip(bank_names, account_numbers, account_types):
            BankAccount.objects.create(
                customer=customer,
                bank_name=bank_name,
                account_number=account_number,
                account_type=account_type
            )

        return redirect('view_customer_detail', customer_id=customer.id)

    return render(request, 'bank_form.html')


""" def add_account(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.customer = customer
            account.save()
            return redirect('view_customer_detail', customer_id=customer.id)
    else:
        form = BankAccountForm()
    return render(request, 'bank_form.html', {'form': form}) """



""" def add_or_edit_bank_accounts(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    BankAccountFormSet = modelformset_factory(BankAccount, form=BankAccountForm, extra=1, can_delete=True)
    
    if request.method == 'POST':
        formset = BankAccountFormSet(request.POST, queryset=BankAccount.objects.filter(customer=customer))
        print(formset)
        if formset.is_valid():
            print('FORMSET IS VALID')
            instances = formset.save(commit=False)
            for instance in instances:
                instance.customer = customer
                instance.save()
            return redirect('view_customer_detail', customer_id=customer.id)
    else:
        formset = BankAccountFormSet(queryset=BankAccount.objects.filter(customer=customer))
    
    return render(request, 'bank_form.html', {'formset': formset, 'customer': customer}) """



""" def add_or_edit_bank_accounts(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    BankAccountFormSet = modelformset_factory(BankAccount, form=BankAccountForm, extra=1, can_delete=True)
    
    if request.method == 'POST':
        formset = BankAccountFormSet(request.POST, queryset=BankAccount.objects.filter(customer=customer))
        print(formset)
        if formset.is_valid():
            print("FORMSET IS VALID")
            instances = formset.save(commit=False)
            for instance in instances:
                if instance.pk:
                    print(f"PRIMARY KEY {instance}")
                    instance.customer = customer
                if instance.DELETE:
                    print(f"DELETED {instance}")
                    instance.delete()
                else:
                    print(f"SAVED {instance}")
                    instance.save()
            return redirect('view_customer_detail', customer_id=customer.id)
    else:
        formset = BankAccountFormSet(queryset=BankAccount.objects.filter(customer=customer))
    
    return render(request, 'bank_form.html', {'formset': formset, 'customer': customer}) """





""" def add_or_edit_bank_accounts(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    BankAccountFormSet = modelformset_factory(BankAccount, form=BankAccountForm, extra=1, can_delete=True)
    
    if request.method == 'POST':
        formset = BankAccountFormSet(request.POST, queryset=BankAccount.objects.filter(customer=customer))
        print(formset)
        if formset.is_valid():
            instances = formset.save(commit=False)
            print(instances)
            for instance in instances:
                print("tHIS IS INSTANCE")
                print(instance)
                print("Processing instance:", instance)
                if instance.pk:
                    instance.customer = customer
                    print("Set customer:", customer)
                if instance.DELETE:
                    print("Instance marked for deletion:", instance)
                    instance.delete()
                else:
                    instance.save()
                    print("Instance saved:", instance)
                instance.save()
            return redirect('view_customer_detail', customer_id=customer.id)
        else:
            print("Formset is not valid.")
            for form in formset:
                print(form.errors)
    else:
        formset = BankAccountFormSet(queryset=BankAccount.objects.filter(customer=customer))
    
    return render(request, 'bank_form.html', {'formset': formset, 'customer': customer}) """


#####################################################################################
#                       API VIEWS
#
######################################################################################


from django.http import JsonResponse


#path('api/customer/<str:customer>/account', views.list_customer_bank_account, name = "list_customer_bank_account")
def list_customer_bank_account(request, customer=''):
    print("DEY DON CALL ME")
    queryset = BankAccount.objects.filter(customer__phone_number=customer)
    serialized_data = BankAccountSerializer(queryset, many=True)
    return JsonResponse(serialized_data.data, safe=False)




from rest_framework import status, generics
from rest_framework.response import Response
from .models import CryptoTransaction, GiftCardTransaction
from .serializers import CryptoTransactionSerializer, GiftCardTransactionSerializer

class CryptoTransactionAPI(generics.GenericAPIView):
    serializer_class = CryptoTransactionSerializer
    queryset = CryptoTransaction.objects.all()

    def get(self, request, transaction_id=None):
        if transaction_id:
            transaction = self.get_object()
            serializer = self.get_serializer(transaction)
            return Response(serializer.data)
        else:
            transactions = self.get_queryset()
            serializer = self.get_serializer(transactions, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, transaction_id=None):
        transaction = self.get_object()
        serializer = self.get_serializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, transaction_id=None):
        transaction = self.get_object()
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GiftCardTransactionAPI(generics.GenericAPIView):
    serializer_class = GiftCardTransactionSerializer
    queryset = GiftCardTransaction.objects.all()

    def get(self, request, transaction_id=None):
        if transaction_id:
            transaction = self.get_object()
            serializer = self.get_serializer(transaction)
            return Response(serializer.data)
        else:
            transactions = self.get_queryset()
            serializer = self.get_serializer(transactions, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, transaction_id=None):
        transaction = self.get_object()
        serializer = self.get_serializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, transaction_id=None):
        transaction = self.get_object()
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


































""" def home(request):
    today = date.today()
    # Fetch recent crypto transactions
    recent_crypto_transactions = CryptoTransaction.objects.all().order_by('-timestamp')[:5]

    # Fetch recent gift card transactions
    recent_giftcard_transactions = GiftCardTransaction.objects.all().order_by('-timestamp')[:5]

    # Combine and sort by date
    recent_transactions = list(recent_crypto_transactions) + list(recent_giftcard_transactions)
    recent_transactions.sort(key=lambda x: x.timestamp, reverse=True)

    # Prepare data for the template
    transactions_data = []
    for transaction in recent_transactions:
        invoice_number = f"INV-{transaction.id}"
        transaction_type = "Crypto" if isinstance(transaction, CryptoTransaction) else "Gift Card"
        customer_name = str(transaction.customer)  # Using the __str__ method of Customer model
        transactions_data.append({
            'date': transaction.timestamp,
            'invoice': invoice_number,
            'customer': customer_name,
            'amount': transaction.amount,
            'status': transaction.settled,
            'type': transaction_type,
        })

    context = {
        'transactions': transactions_data,
    }

    return render(request, 'index.html', context)
 """

""" def enter_transaction_view(request):
    return render(request, 'transaction_form.html') """



""" def enter_transaction_view(request):
    if request.method == 'POST':
        if 'crypto_submit' in request.POST:
            crypto_form = CryptoTransactionForm(request.POST)
            giftcard_form = GiftCardTransactionForm()
            if crypto_form.is_valid():
                crypto_form.save()
                return redirect('home')
                return redirect('success_url')
        elif 'giftcard_submit' in request.POST:
            giftcard_form = GiftCardTransactionForm(request.POST)
            crypto_form = CryptoTransactionForm()
            if giftcard_form.is_valid():
                giftcard_form.save()
                return redirect('home')
                return redirect('success_url')
    else:
        crypto_form = CryptoTransactionForm()
        giftcard_form = GiftCardTransactionForm()

    return render(request, 'transaction_form.html', {
        'crypto_form': crypto_form,
        'giftcard_form': giftcard_form
    }) """




""" def enter_transaction_view(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'crypto_form':
            crypto_form = CryptoTransactionForm(request.POST)
            giftcard_form = GiftCardTransactionForm()
            if crypto_form.is_valid():
                crypto_form.save()
                # Add success message or redirection if needed
        elif form_type == 'giftcard_form':
            giftcard_form = GiftCardTransactionForm(request.POST)
            crypto_form = CryptoTransactionForm()
            if giftcard_form.is_valid():
                giftcard_form.save()
                # Add success message or redirection if needed
    else:
        crypto_form = CryptoTransactionForm()
        giftcard_form = GiftCardTransactionForm()
        
    return render(request, 'transaction_form.html', {
        'crypto_form': crypto_form,
        'giftcard_form': giftcard_form
    })
 """