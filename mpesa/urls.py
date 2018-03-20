from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^get_token/$',
        view=authenticate,
        name="get-mpesa-token-request",),
    # url(r'^create_response/$',
    #     view=transactions_record,
    #     name="add-transaction-response",),
    url(r'^create_b_to_b_transaction/$',
        view=create_b_to_b_transaction,
        name="create_transaction",),
]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])

# url end points to be effected

# create_b_to_c_transaction
# create_b_to_b_transaction
# register_c_2_b_url
# check_account_balance
# check_transaction_status
# transaction_reversal
# initiate_lipa_na_mpesa_online_transaction
# query_lipa_na_mpesa_online_transaction_status

# create_occasion
# create_mpesa_command_id
# create_company_short_code_or_number
# create_initiator_name
# create_transaction_type
# create_customer
# create_identifier_type

# OccasionDetailAPIView
# MpesaCommandIdDetailAPIView
# MpesaShortCodeOrNumberDetailAPIView
# InitiatorNameDetailAPIView
# TransactionTypeDetailAPIView
# CustomerDetailAPIView
# IdentifierTypeDetailAPIView

# OccasionListView
# MpesaCommandIdListView
# MpesaShortCodeOrNumberListView
# InitiatorNameListView
# TransactionTypeListView
# CustomerListView
# IdentifierTypeListView
# TransactionListView
# TransactionResponseListView
# RegistrationListView
