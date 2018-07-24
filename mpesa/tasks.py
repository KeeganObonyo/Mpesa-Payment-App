# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery import task
import requests
from rest_framework.response import Response
from .models import TransactionResponse

@task
def send_create_b2c_transaction(request):
    """
    Task to send create b2c transaction request
    """
    api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
    headers = {"Authorization": "Bearer %s" % access_token}

    response = requests.post(api_url, json=request, headers=headers)
    response_description = response['ResponseDescription']
    originator_conversation_id = response['OriginatorConversationID ']
    conversation_id = response['ConversationID']
    merchant_request_id = response['MerchantRequestID']
    checkout_request_id = response['CheckoutRequestID']
    response_code = response['ResponseCode']
    result_description = response['ResultDesc']
    result_code = response['ResultCode']
    TransactionResponse.objects.create(
        transaction_feedback=response_description,
        transaction=transaction,
        originator_conversation_id=originator_conversation_id,
        conversation_id=conversation_id,
        merchant_request_id=merchant_request_id,
        checkout_request_id=checkout_request_id,
        response_code=response_code,
        result_description=result_description,
        result_code=result_code)