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
