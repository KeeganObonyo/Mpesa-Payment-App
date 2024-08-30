# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery import shared_task
import requests
from rest_framework.response import Response
from .models import TransactionResponse

@shared_task
def send_create_b2c_transaction(request,access_token):
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

@shared_task
def send_create_b2b_transaction(request,access_token):
    """
    Task to send create b2b transaction request asynchronously
    """
    api_url = "https://sandbox.safaricom.co.ke/mpesa/b2b/v1/paymentrequest"
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

@shared_task
def send_register_c_to_b_url(request,access_token):
    """
    Task to send create ctob transaction request asynchronously
    """
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
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

@shared_task
def send_check_account_balance(request,access_token):
    """
    Task to check accoubt balance asynchronously
    """
    api_url = "https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query"
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

@shared_task
def send_check_transaction_status(request,access_token):
    """
    Task to check transaction status asynchronously
    """
    api_url = "https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query"
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

@shared_task
def send_transaction_reversal(request,access_token):
    """
    Task to send create transaction reversal request asynchronously
    """
    api_url = "https://sandbox.safaricom.co.ke/mpesa/reversal/v1/request"
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


@shared_task
def send_initiate_lipa_na_mpesa_online(request,access_token):
    """
    Task to initiate lipa na mpesa request online asynchronous
    """
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
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

@shared_task
def send_query_lipa_na_mpesa_online_status(request,access_token):
    """
    Task to check stk push transaction status
    """
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"
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
