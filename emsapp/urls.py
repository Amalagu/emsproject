from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('transaction', views.add_edit_transaction_view, name='add_edit_transaction_view' ),
    path('transaction/', views.enter_transaction_view, name='enter_transaction'),
    path('transaction/<str:transaction_type>/', views.enter_transaction_view, name='enter_transaction_type'),
    path('transaction/<str:transaction_type>/<int:transaction_id>/', views.enter_transaction_view, name='edit_transaction'),



    #path('transaction_detail', views.view_transaction_detail, name='view_transaction_detail' ),
    path('transaction_detail/<str:transaction_type>/<int:transaction_id>/', views.view_transaction_detail, name='view_transaction_detail'),
    path('filter_transactions/', views.transactions_view, name='filter_transactions'),
    path('customers/', views.all_customers, name='all_customers'),
    path('customer/add/', views.add_or_edit_customer, name='add_customer'),
    path('customer/edit/<int:customer_id>/', views.add_or_edit_customer, name='edit_customer'),
    path('customer/<int:customer_id>/', views.view_customer_detail, name='view_customer_detail'),
    #path('customer/<int:customer_id>/edit/', views.edit_customer, name='edit_customer'),
    path('customer/<int:customer_id>/delete/', views.delete_customer, name='delete_customer'),
    path('customer/<int:customer_id>/add_account/', views.add_account, name='add_account'),
    path('transaction/delete/<str:transaction_type>/<int:transaction_id>/', views.delete_transaction_view, name='delete_transaction'),
    
    #API's
    path('api/customer/<str:customer>/account/', views.list_customer_bank_account, name = "list_customer_bank_account")
]



from django.urls import path
from .views import CryptoTransactionAPI, GiftCardTransactionAPI

urlpatterns += [
    path('api/crypto/', CryptoTransactionAPI.as_view(), name='crypto-list-create'),
    path('api/crypto/<int:transaction_id>/', CryptoTransactionAPI.as_view(), name='crypto-detail'),
    path('api/giftcard/', GiftCardTransactionAPI.as_view(), name='giftcard-list-create'),
    path('api/giftcard/<int:transaction_id>/', GiftCardTransactionAPI.as_view(), name='giftcard-detail'),
]





""" urlpatterns = [
    # URL for entering a new crypto transaction
    path('transaction/crypto/new/', views.add_edit_transaction_view, {'transaction_type': 'crypto'}, name='new_crypto_transaction'),

    # URL for editing an existing crypto transaction
    path('transaction/crypto/edit/<int:transaction_id>/', views.add_edit_transaction_view, {'transaction_type': 'crypto'}, name='edit_crypto_transaction'),

    # URL for entering a new gift card transaction
    path('transaction/giftcard/new/', views.add_edit_transaction_view, {'transaction_type': 'giftcard'}, name='new_giftcard_transaction'),

    # URL for editing an existing gift card transaction
    path('transaction/giftcard/edit/<int:transaction_id>/', views.add_edit_transaction_view, {'transaction_type': 'giftcard'}, name='edit_giftcard_transaction'),
]
 """
