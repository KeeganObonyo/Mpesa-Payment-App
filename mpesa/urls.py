from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('b2b/transaction/', CreateBToBTransaction.as_view(), name="create_b_2_b_transaction"),
    path('b2c/transaction/', CreateBToCTransaction.as_view(), name="create_b_2_c_transaction"),
    path('register/c2b/url/', RegisterCToBUrl.as_view(), name="register_c_2_b_url"),
    path('accountbalance/transaction/', CheckAccountBalance.as_view(), name="check_account_balance"),
    path('check/transaction/status/', CheckTransactionStatus.as_view(), name="check_transaction_status"),
    path('reversal/transaction', TransactionReversal.as_view(), name="transaction_reversal"),
    path('lipanampesa/online/', InitiateLipaNaMpesaTransaction.as_view(), name="initiate_lipa_na_mpesa_online_transaction"),
    path('lipanampesa/online/transaction/status', QueryLipaNaMpesaOnlineTransactionStatus.as_view(), name="query_lipa_na_mpesa_online_transaction_status"),
    path('create/occassion/', CreateOccassion.as_view(), name="create_occasion"),
    path('create/mpesa/command/id/', CreateMpesaCommandId.as_view(), name="create_mpesa_command_id"),
    path('create/company/shortcodeornumber/', CreateCompanyShortCodeOrNumber.as_view(), name="create_company_short_code_or_number"),
    path('create/initiator/name/', CreateInitiatorName.as_view(), name="create_initiator_name"),
    path('create/transaction/type/', CreateTransactionType.as_view(), name="create_transaction_type"),
    path('create/initiator/type/', CreateInitiatorType.as_view(), name="create_initiator_type"),

    re_path(r'^occassion/detail/(?P<pk>\d+)/$', OccasionDetailAPIView.as_view(), name='occasion-detail'),
    re_path(r'^mpesa/commandid/detail/(?P<pk>\d+)/$', MpesaCommandIdDetailAPIView.as_view(), name='mpesa-commandid-detail'),
    re_path(r'^mpesa/shortcodeornumber/detail/(?P<pk>\d+)/$', MpesaShortCodeOrNumberDetailAPIView.as_view(), name='shortcodeornumber-detail'),
    re_path(r'^initiator/name/detail/(?P<pk>\d+)/$', InitiatorNameDetailAPIView.as_view(), name='initiator-name-detail'),
    re_path(r'^transaction/type/detail/(?P<pk>\d+)/$', TransactionTypeDetailAPIView.as_view(), name='transaction-type-detail'),
    re_path(r'^identifier/type/detail/(?P<pk>\d+)/$', IdentifierTypeDetailAPIView.as_view(), name='identifier-type-detail'),

    path('occassion/list/', OccasionListView.as_view(), name='occasion-list'),
    path('mpesacommandid/list/', MpesaCommandIdListView.as_view(), name='mpesa-commandid-list'),
    path('shortcodeornumber/list/', MpesaShortCodeOrNumberListView.as_view(), name='shortcodeornumber-list'),
    path('initiatorname/list/', InitiatorNameListView.as_view(), name='initiatorname-list'),
    path('transactiontype/list/', TransactionTypeListView.as_view(), name='transactiontype-list'),
    path('identifiertype/list/', IdentifierTypeListView.as_view(), name='identifiertype-list'),
    path('transaction/list/', TransactionListView.as_view(), name='transaction-list'),
    path('transactionresponse/list/', TransactionResponseListView.as_view(), name='transactionresponse-list'),
    path('registration/list/', RegistrationListView.as_view(), name='registration-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
