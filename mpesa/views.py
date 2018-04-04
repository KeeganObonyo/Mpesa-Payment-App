import requests
from rest_framework import status, generics
from rest_framework.decorators import *
from rest_framework.renderers import *
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)
import json
from django.http import Http404
# from m2rypto import RSA, X509
import base64
# from base64 import b64encode
# To authenticate your app and get an OAuth access token, use this code.
# An access token expires in 3600 seconds or 1 hour


from requests.auth import HTTPBasicAuth


class Authenticate(APIView):

    def get(self, request, format=None):
        consumer_key = "dJjjF6lieZzA62MRlGnd5YSnBBIxcAE1"
        consumer_secret = "kJZcB2pDoulDOwOu"
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

        r = requests.get(api_URL, auth=HTTPBasicAuth(
            consumer_key, consumer_secret))
        data = r.json()
        token = data['access_token']

        return Response(token, status=status.HTTP_200_OK)


INITIATOR_PASS = "YOUR_PASSWORD"
CERTIFICATE_FILE = "PATH_TO_CERTIFICATE_FILE"

# Base64 encoded string of the Security Credential, which is encrypted
# using M-Pesa public key and validates the transaction on M-Pesa Core
# system.


def Password():
    cipher = (
        INITIATOR_PASS, code_b, time)
    return b64encode(cipher)


def encryptInitiatorPassword():
    cert_file = open(CERTIFICATE_FILE, 'r')
    cert_data = cert_file.read()  # read certificate file
    cert_file.close()

    cert = X509.load_cert_string(cert_data)
    # pub_key = X509.load_cert_string(cert_data)
    pub_key = cert.get_pubkey()
    rsa_key = pub_key.get_rsa()
    cipher = rsa_key.public_encrypt(INITIATOR_PASS, RSA.pkcs1_padding)
    return b64encode(cipher)


class CreateBToCTransaction(APIView):

    def post(self, *args, **kwargs):
        # company to customer transaction based phone no and shortcode
        access_token = authenticate()
        try:
            try:
                party_a = CompanyCodeOrNumber.objects.get(
                    id=request.data['company_short_code'])
                initiator_name = InitiatorName.objects.get(
                    id=request.data['company_name'])
                transaction_type = TransactionType.objects.get(
                    id=request.data['transaction_type'])
                command_id = MpesaCommandId.objects.get(
                    id=request.data['command_id'])
                occasion = Occasion.objects.get(id=request.data['occasion'])
                amount = request.data['amount'],
                remarks = request.data['remarks'],
                party_b = CompanyCodeOrNumber.objects.get(
                    id=request.data['phone_no']),
                transaction = Transaction.objects.create(
                    amount=amount,
                    comments=comments,
                    party_b=party_b,
                    Party_a=Party_a,
                    command_id=command_id,
                    transaction_type=transaction_type,
                    initiator_name=initiator_name,
                    occasion=occasion)
                initiator = encryptInitiatorPassword()
                code_a = CompanyCodeOrNumber.objects.filter(
                    id=party_a).values('name')[0]['name']
                code_b = CompanyCodeOrNumber.objects.filter(
                    id=party_b).values('name')[0]['name']
                name = InitiatorName.objects.filter(
                    id=initiator_name).values('name')[0]['name']
                com_id = MpesaCommandId.objects.filter(
                    id=command_id).values('name')[0]['name']
                occ = Occasion.objects.filter(
                    id=occasion).values('name')[0]['name']

            except:
                raise Http404
            api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
            headers = {"Authorization": "Bearer %s" % access_token}
            request = {
                "InitiatorName": name,
                "SecurityCredential": initiator,
                "CommandID": com_id,
                "Amount": amount,
                "PartyA": code_a,
                "PartyB": code_b,
                "Remarks": remarks,
                "QueueTimeOutURL": "/",
                "ResultURL": "/",
                "Occasion": occ
            }

            response = requests.post(api_url, json=request, headers=headers)
            response_description = response['ResponseDescription']
            originator_conversation_id = response['OriginatorConversationID ']
            conversation_id = response['ConversationID']
            merchant_request_id = response['MerchantRequestID']
            checkout_request_id = response['CheckoutRequestID']
            response_code = response['ResponseCode']
            result_description = response['ResultDesc']
            result_code = response['ResultCode']
            transaction_response = TransactionResponse.objects.create(
                transaction_feedback=response_description,
                transaction=transaction,
                originator_conversation_id=originator_conversation_id,
                conversation_id=conversation_id,
                merchant_request_id=merchant_request_id,
                checkout_request_id=checkout_request_id,
                response_code=response_code,
                result_description=result_description,
                result_code=result_code)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(responses, status=status.HTTP_201_CREATED)


class CreateBToBTransaction(APIView):

    def post(self, *args, **kwargs):
        # company to company transaction based on short codes
        access_token = authenticate()
        try:
            try:
                party_a = CompanyCodeOrNumber.objects.get(
                    id=request.data['company_short_code'])
                initiator_name = InitiatorName.objects.get(
                    id=request.data['company_name'])
                transaction_type = TransactionType.objects.get(
                    id=request.data['transaction_type'])
                command_id = MpesaCommandId.objects.get(
                    id=request.data['command_id'])
                occasion = Occasion.objects.get(id=request.data['occasion'])
                identifier_type_a = IdentifierType.objects.get(
                    id='identifier_type')
                identifier_type_b = IdentifierType.objects.get(
                    id='identifier_type')
                amount = request.data['amount'],
                remarks = request.data['remarks'],
                party_b = CompanyCodeOrNumber.objects.get(
                    id=request.data['phone_no']),
                transaction = Transaction.objects.create(
                    amount=amount,
                    remarks=remarks,
                    party_b=party_b,
                    Party_a=Party_a,
                    command_id=command_id,
                    transaction_type=transaction_type,
                    initiator_name=initiator_name,
                    occasion=occasion)
                initiator = encryptInitiatorPassword()
                com_id = MpesaCommandId.objects.filter(
                    id=command_id).values('name')[0]['name']
                party_a = CompanyCodeOrNumber.objects.filter(
                    id=party_a).values('name')[0]['name']
                party_b = CompanyCodeOrNumber.objects.filter(
                    id=party_b).values('name')[0]['name']
                name = InitiatorName.objects.filter(
                    id=initiator_name).values('name')[0]['name']
                id_type_a = IdentifierType.objects.filter(
                    id=identifier_type_a).values('name')[0]['name']
                id_type_b = IdentifierType.objects.filter(
                    id=identifier_type_b).values('name')[0]['name']
            except:
                raise Http404
            api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
            headers = {"Authorization": "Bearer %s" % access_token}
            request = {
                "Initiator": name,
                "SecurityCredential": initiator,
                "CommandID": com_id,
                "SenderIdentifierType": id_type_a,
                "RecieverIdentifierType": id_type_b,
                "Amount": amount,
                "PartyA": party_a,
                "PartyB": party_b,
                "AccountReference": com_id,
                "Remarks": remarks,
                "QueueTimeOutURL": "/",
                "ResultURL": "/"
            }

            response = requests.post(api_url, json=request, headers=headers)
            response_description = response['ResponseDescription']
            originator_conversation_id = response['OriginatorConversationID ']
            conversation_id = response['ConversationID']
            merchant_request_id = response['MerchantRequestID']
            checkout_request_id = response['CheckoutRequestID']
            response_code = response['ResponseCode']
            result_description = response['ResultDesc']
            result_code = response['ResultCode']
            transaction_response = TransactionResponse.objects.create(
                transaction_feedback=response_description,
                transaction=transaction,
                originator_conversation_id=originator_conversation_id,
                conversation_id=conversation_id,
                merchant_request_id=merchant_request_id,
                checkout_request_id=checkout_request_id,
                response_code=response_code,
                result_description=result_description,
                result_code=result_code)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(responses, status=status.HTTP_201_CREATED)


class RegisterCToBUrl(APIView):

    def post(self, *args, **kwargs):
        # The C2B Register URL API registers the 3rd party’s confirmation and validation URLs to M-Pesa ;
        # which then maps these URLs to the 3rd party shortcode.
        # Whenever M-Pesa receives a transaction on the shortcode,
        # M-Pesa triggers a validation request against the validation URL.
        # The 3rd party system responds to M-Pesa with a validation response (either a success or an error code).
        # The response expected is the success code the 3rd party
        access_token = authenticate()
        try:
            try:
                initiator_name = InitiatorName.objects.get(
                    id=request.data['company_name'])
                party_b = CompanyCodeOrNumber.objects.get(
                    id=request.data['phone_no']),
                confirmation_url = request.data['confirmation_url']
                validation_url = request.data['confirmation_url']
                registration = Registration.objects.create(
                    company=party_b,
                    initiator_name=initiator_name,
                    confirmation_url=confirmation_url,
                    validation_url=validation_url)
            except:
                raise Http404
                party_b = CompanyCodeOrNumber.objects.filter(
                    id=party_b).values('name')[0]['name']

            api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
            headers = {"Authorization": "Bearer %s" % access_token}
            request = {"ShortCode": party_b,
                       "ResponseType": "json",
                       "ConfirmationURL": confirmation_url,
                       #"http://ip_address:port/confirmation",
                       "ValidationURL": validation_url,
                       # "http://ip_address:port/validation_url"
                       }
            response = requests.post(api_url, json=request, headers=headers)
            response_description = response['ResponseDescription']
            originator_conversation_id = response['OriginatorConversationID ']
            conversation_id = response['ConversationID']
            merchant_request_id = response['MerchantRequestID']
            checkout_request_id = response['CheckoutRequestID']
            response_code = response['ResponseCode']
            result_description = response['ResultDesc']
            result_code = response['ResultCode']
            transaction_response = TransactionResponse.objects.create(
                transaction_feedback=response_description,
                transaction=transaction,
                originator_conversation_id=originator_conversation_id,
                conversation_id=conversation_id,
                merchant_request_id=merchant_request_id,
                checkout_request_id=checkout_request_id,
                response_code=response_code,
                result_description=result_description,
                result_code=result_code)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(responses, status=status.HTTP_201_CREATED)


class CheckAccountBalance(APIView):

    def post(self, *args, **kwargs):
        # company to company transaction based on short codes
        access_token = authenticate()
        try:
            try:
                party_a = CompanyCodeOrNumber.objects.get(
                    id=request.data['company_short_code'])
                initiator_name = InitiatorName.objects.get(
                    id=request.data['company_name'])
                command_id = MpesaCommandId.objects.get(
                    id=request.data['command_id'])
                remarks = request.data['remarks'],
                command_id = MpesaCommandId.objects.get(
                    id=request.data['command_id'])
                transaction = Transaction.objects.create(
                    command_id=command_id,
                    Party_a=Party_a,
                    initiator_name=initiator_name)
                initiator = encryptInitiatorPassword()
                com_id = MpesaCommandId.objects.filter(
                    id=command_id).values('name')[0]['name']
                party_a = CompanyCodeOrNumber.objects.filter(
                    id=party_a).values('name')[0]['name']
                name = InitiatorName.objects.filter(
                    id=initiator_name).values('name')[0]['name']
            except:
                raise Http404
            api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
            headers = {"Authorization": "Bearer %s" % access_token}
            request = {"Initiator": name,
                       "SecurityCredential": initiator,
                       "CommandID": com_id,
                       "PartyA": party_a,
                       "IdentifierType": "4",
                       "Remarks": remarks,
                       "QueueTimeOutURL": "https://ip_address:port/timeout_url",
                       "ResultURL": "https://ip_address:port/result_url"
                       }
            response = requests.post(api_url, json=request, headers=headers)
            response_description = response['ResponseDescription']
            originator_conversation_id = response['OriginatorConversationID ']
            conversation_id = response['ConversationID']
            merchant_request_id = response['MerchantRequestID']
            checkout_request_id = response['CheckoutRequestID']
            response_code = response['ResponseCode']
            result_description = response['ResultDesc']
            result_code = response['ResultCode']
            transaction_response = TransactionResponse.objects.create(
                transaction_feedback=response_description,
                transaction=transaction,
                originator_conversation_id=originator_conversation_id,
                conversation_id=conversation_id,
                merchant_request_id=merchant_request_id,
                checkout_request_id=checkout_request_id,
                response_code=response_code,
                result_description=result_description,
                result_code=result_code)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(responses, status=status.HTTP_201_CREATED)


class CheckTransactionStatus(APIView):

    def post(self, *args, **kwargs):
        # company to company transaction based on short codes
        access_token = authenticate()
        try:
            try:
                party_a = CompanyCodeOrNumber.objects.get(
                    id=request.data['create_company_short_code_or_number'])
                initiator_name = InitiatorName.objects.get(
                    id=request.data['company_name'])
                transaction_type = TransactionType.objects.get(
                    id=request.data['transaction_type'])
                command_id = MpesaCommandId.objects.get(
                    id=request.data['command_id'])
                amount = request.data['amount'],
                remarks = request.data['remarks'],
                party_b = CompanyCodeOrNumber.objects.get(
                    id=request.data['phone_no']),
                transaction = Transaction.objects.create(
                    amount=amount,
                    remarks=remarks,
                    party_b=party_b,
                    Party_a=Party_a,
                    command_id=command_id,
                    transaction_type=transaction_type,
                    initiator_name=initiator_name,
                    occasion=occasion)
                initiator = encryptInitiatorPassword()
                com_id = MpesaCommandId.objects.filter(
                    id=command_id).values('name')[0]['name']
                party_a = CompanyCodeOrNumber.objects.filter(
                    id=party_a).values('name')[0]['name']
                party_b = CompanyCodeOrNumber.objects.filter(
                    id=party_b).values('name')[0]['name']
                name = InitiatorName.objects.filter(
                    id=initiator_name).values('name')[0]['name']
            except:
                raise Http404
            api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
            headers = {"Authorization": "Bearer %s" % access_token}
            request = {
                "Initiator": name,
                "SecurityCredential": initiator,
                "CommandID": com_id,
                "TransactionID": party_b,
                "PartyA": party_a,
                "IdentifierType": "1",
                "ResultURL": "https://ip_address:port/result_url",
                "QueueTimeOutURL": "https://ip_address:port/timeout_url",
                "Remarks": remarks
            }

            response = requests.post(api_url, json=request, headers=headers)
            response_description = response['ResponseDescription']
            originator_conversation_id = response['OriginatorConversationID ']
            conversation_id = response['ConversationID']
            merchant_request_id = response['MerchantRequestID']
            checkout_request_id = response['CheckoutRequestID']
            response_code = response['ResponseCode']
            result_description = response['ResultDesc']
            result_code = response['ResultCode']
            transaction_response = TransactionResponse.objects.create(
                transaction_feedback=response_description,
                transaction=transaction,
                originator_conversation_id=originator_conversation_id,
                conversation_id=conversation_id,
                merchant_request_id=merchant_request_id,
                checkout_request_id=checkout_request_id,
                response_code=response_code,
                result_description=result_description,
                result_code=result_code)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(responses, status=status.HTTP_201_CREATED)


class TransactionReversal(APIView):

    def post(self, *args, **kwargs):
        # company to customer transaction based phone no and shortcode
        access_token = authenticate()
        try:
            try:
                party_a = CompanyCodeOrNumber.objects.get(
                    id=request.data['company_short_code'])
                initiator_name = InitiatorName.objects.get(
                    id=request.data['company_name'])
                transaction_type = TransactionType.objects.get(
                    id=request.data['transaction_type'])
                command_id = MpesaCommandId.objects.get(
                    id=request.data['command_id'])
    #            occasion = Occasion.objects.get(id=request.data['occasion'])
                amount = request.data['amount'],
                remarks = request.data['remarks'],
                party_b = CompanyCodeOrNumber.objects.get(
                    id=request.data['phone_no']),
                transaction = Transaction.objects.create(
                    amount=amount,
                    comments=comments,
                    party_b=party_b,
                    Party_a=Party_a,
                    command_id=command_id,
                    transaction_type=transaction_type,
                    initiator_name=initiator_name,
                    occasion=occasion)
                initiator = encryptInitiatorPassword()
                code_a = CompanyCodeOrNumber.objects.filter(
                    id=party_a).values('name')[0]['name']
                code_b = CompanyCodeOrNumber.objects.filter(
                    id=party_b).values('name')[0]['name']
                name = InitiatorName.objects.filter(
                    id=initiator_name).values('name')[0]['name']
                com_id = MpesaCommandId.objects.filter(
                    id=command_id).values('name')[0]['name']

            except:
                raise Http404
            api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
            headers = {"Authorization": "Bearer %s" % access_token}
            request = {"Initiator": name,
                       "SecurityCredential": initiator,
                       "CommandID": com_id,
                       "TransactionID": code_b,
                       "Amount": amount,
                       "PartyA": code_a,
                       "RecieverIdentifierType": "4",
                       "ResultURL": "https://ip_address:port/result_url",
                       "QueueTimeOutURL": "https://ip_address:port/timeout_url",
                       "Remarks": remarks,
                       "Occasion": " "
                       }

            response = requests.post(api_url, json=request, headers=headers)
            response_description = response['ResponseDescription']
            originator_conversation_id = response['OriginatorConversationID ']
            conversation_id = response['ConversationID']
            merchant_request_id = response['MerchantRequestID']
            checkout_request_id = response['CheckoutRequestID']
            response_code = response['ResponseCode']
            result_description = response['ResultDesc']
            result_code = response['ResultCode']
            transaction_response = TransactionResponse.objects.create(
                transaction_feedback=response_description,
                transaction=transaction,
                originator_conversation_id=originator_conversation_id,
                conversation_id=conversation_id,
                merchant_request_id=merchant_request_id,
                checkout_request_id=checkout_request_id,
                response_code=response_code,
                result_description=result_description,
                result_code=result_code)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(responses, status=status.HTTP_201_CREATED)


class InitiateLipaNaMpesaTransaction(APIView):

    def post(self, *args, **kwargs):
        # Lipa na M-Pesa Online Payment API is
        # used to initiate a M-Pesa transaction
        # on behalf of a customer using STK Push
        access_token = authenticate()
        try:
            try:
                party_a = CompanyCodeOrNumber.objects.get(
                    id=request.data['company_short_code'])
                initiator_name = InitiatorName.objects.get(
                    id=request.data['company_name'])
                transaction_type = TransactionType.objects.get(
                    id=request.data['transaction_type'])
                command_id = MpesaCommandId.objects.get(
                    id=request.data['command_id'])
                # occasion = Occasion.objects.get(id=request.data['occasion'])
                amount = request.data['amount'],
                remarks = request.data['remarks'],
                party_b = CompanyCodeOrNumber.objects.get(
                    id=request.data['phone_no']),
                transaction = Transaction.objects.create(
                    amount=amount,
                    remarks=remarks,
                    party_b=party_b,
                    Party_a=Party_a,
                    command_id=command_id,
                    transaction_type=transaction_type,
                    initiator_name=initiator_name)
                code_a = CompanyCodeOrNumber.objects.filter(
                    id=party_a).values('name')[0]['name']
                code_b = CompanyCodeOrNumber.objects.filter(
                    id=party_b).values('name')[0]['name']
                com_id = MpesaCommandId.objects.filter(
                    id=command_id).values('name')[0]['name']
                t_type = TransactionType.objects.filter(
                    id=transaction_type).values('name')[0]['name']
                time = Transaction.objects.filter(
                    id=transaction).values('created')[0]['created']

            except:
                raise Http404
            password = Password(code_b, time)
            api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
            headers = {"Authorization": "Bearer %s" % access_token}
            request = {
                "BusinessShortCode": code_b,
                "Password": password,
                "Timestamp": time,
                "TransactionType": t_type,
                "Amount": amount,
                "PartyA": code_a,
                "PartyB": code_b,
                "PhoneNumber": code_a,
                "CallBackURL": "https://ip_address:port/callback",
                "AccountReference": com_id,
                "TransactionDesc": remarks
            }

            response = requests.post(api_url, json=request, headers=headers)
            response_description = response['ResponseDescription']
            originator_conversation_id = response['OriginatorConversationID ']
            conversation_id = response['ConversationID']
            merchant_request_id = response['MerchantRequestID']
            checkout_request_id = response['CheckoutRequestID']
            response_code = response['ResponseCode']
            result_description = response['ResultDesc']
            result_code = response['ResultCode']
            transaction_response = TransactionResponse.objects.create(
                transaction_feedback=response_description,
                transaction=transaction,
                originator_conversation_id=originator_conversation_id,
                conversation_id=conversation_id,
                merchant_request_id=merchant_request_id,
                checkout_request_id=checkout_request_id,
                response_code=response_code,
                result_description=result_description,
                result_code=result_code)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(responses, status=status.HTTP_201_CREATED)


class QueryLipaNaMpesaOnlineTransactionStatus(APIView):

    def post(self, *args, **kwargs):
        # Lipa na M-Pesa Online Payment API is
        # used to initiate a M-Pesa transaction
        # on behalf of a customer using STK Push
        access_token = authenticate()
        try:
            try:
                initiator_name = InitiatorName.objects.get(
                    id=request.data['company_name'])
                transaction_type = TransactionType.objects.get(
                    id=request.data['transaction_type'])
                party_b = CompanyCodeOrNumber.objects.get(
                    id=request.data['phone_no']),
                transaction = Transaction.objects.create(
                    amount=amount,
                    remarks=remarks,
                    party_b=party_b,
                    transaction_type=transaction_type,
                    initiator_name=initiator_name)
                code_b = CompanyCodeOrNumber.objects.filter(
                    id=party_b).values('name')[0]['name']
                time = Transaction.objects.filter(
                    id=transaction).values('created')[0]['created']
            except:
                raise Http404
            password = Password(code_b, time)
            api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
            headers = {"Authorization": "Bearer %s" % access_token}
            request = {
                "BusinessShortCode": code_b,
                "Password": password,
                "Timestamp": time,
                "CheckoutRequestID": checkout_request_ids,
            }

            response = requests.post(api_url, json=request, headers=headers)
            response_description = response['ResponseDescription']
            originator_conversation_id = response['OriginatorConversationID ']
            conversation_id = response['ConversationID']
            merchant_request_id = response['MerchantRequestID']
            checkout_request_id = response['CheckoutRequestID']
            response_code = response['ResponseCode']
            result_description = response['ResultDesc']
            result_code = response['ResultCode']
            transaction_response = TransactionResponse.objects.create(
                transaction_feedback=response_description,
                transaction=transaction,
                originator_conversation_id=originator_conversation_id,
                conversation_id=conversation_id,
                merchant_request_id=merchant_request_id,
                checkout_request_id=checkout_request_id,
                response_code=response_code,
                result_description=result_description,
                result_code=result_code)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(responses, status=status.HTTP_201_CREATED)


class CreateOccassion(api_view):

    def post(self, *args, **kwargs):
        occassion = Occassion.objects.create(name=request.data['occasion'])
        return Response(responses, status=status.HTTP_201_CREATED)


class CreateMpesaCommandId(APIView):

    def post(self, *args, **kwargs):
        command_id = MpesaCommandId.objects.create(
            name=request.data['command_id'])
        return Response(responses, status=status.HTTP_201_CREATED)


class CreateCompanyShortCodeOrNumber(APIView):

    def post(self, *args, **kwargs):
        shortcode = CompanyShortCodeOrNumber.objects.create(
            name=request.data['short_code'])
        return Response(responses, status=status.HTTP_201_CREATED)


class CreateInitiatorName(APIView):

    def post(self, *args, **kwargs):
        initiator_name = InitiatorName.objects.create(
            name=request.data['initiator_name'])
        return Response(responses, status=status.HTTP_201_CREATED)


class CreateTransactionType(APIView):

    def post(self, *args, **kwargs):
        transaction_type = TransactionType.objects.create(
            name=request.data['transaction_type'])
        return Response(responses, status=status.HTTP_201_CREATED)


class CreateCustomer(ApiView):

    def post(self, *args, **kwargs):
        number = CompanyShortCodeOrNumber.objects.get(
            id=request.data['number'])
        customer = Customer.objects.create(
            name=request.data['transaction_type'],
            number=number)
        return Response(responses, status=status.HTTP_201_CREATED)


class CreateInitiatorType(APIView):

    def post(self, *args, **kwargs):
        transaction_type = IdentifierType.objects.create(
            name=request.data['transaction_type'])
        return Response(response, status=status.HTTP_201_CREATED)


class OccasionListView(generics.ListAPIView):
    serializer_class = OccassionSerializer
    queryset = Occassion.objects.all()

    def list(self, request):
        try:
            occassions = Occassion.objects.all()
        except:
            raise Http404
        serializer = OccasionSerializer(
            occassions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OccasionDetailAPIView(DestroyModelMixin,
                            UpdateModelMixin,
                            generics.RetrieveAPIView):

    def get_object(self, pk):
        try:
            return Occassion.objects.get(pk=pk)
        except Occassion.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = OccassionSerializer(occassion)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        serializer = OccasionSerializer(
            occassion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            occassion = self.get_object(pk)
            occassion.delete()
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


class MpesaCommandIdListView(generics.ListAPIView):
    serializer_class = MpesaCommandIdSerializer
    queryset = MpesaCommandId.objects.all()

    def list(self, request):
        try:
            command_ids = MpesaCommandId.objects.all()
        except:
            raise Http404
        serializer = MpesaCommandIdSerializer(
            command_ids, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MpesaCommandIdDetailAPIView(DestroyModelMixin,
                                  UpdateModelMixin,
                                  generics.RetrieveAPIView):

    def get_object(self, pk):
        try:
            return MpesaCommandId.objects.get(pk=pk)
        except MpesaCommandId.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = MpesaCommandIdSerializer(command_id)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        serializer = MpesaCommandIdSerializer(
            command_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            command_id = self.get_object(pk)
            command_id.delete()
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


class MpesaShortCodeOrNumberListView(generics.ListAPIView):
    serializer_class = CompanyShortCodeOrNumberSerializer
    queryset = CompanyShortCodeOrNumber.objects.all()

    def list(self, request):
        try:
            company_codes_or_nos = CompanyShortCodeOrNumber.objects.all()
        except:
            raise Http404
        serializer = CompanyShortCodeOrNumberSerializer(
            company_codes_or_nos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MpesaShortCodeOrNumberDetailAPIView(DestroyModelMixin,
                                          UpdateModelMixin,
                                          generics.RetrieveAPIView):

    def get_object(self, pk):
        try:
            return CompanyShortCodeOrNumber.objects.get(pk=pk)
        except CompanyShortCodeOrNumber.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = CompanyShortCodeOrNumberSerializer(companycode_or_no)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        serializer = CompanyShortCodeOrNumberSerializer(
            companycode_or_no, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            companycode_or_no = self.get_object(pk)
            companycode_or_no.delete()
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


class InitiatorNameListView(generics.ListAPIView):
    serializer_class = InitiatorNameSerializer
    queryset = InitiatorName.objects.all()

    def list(self, request):
        try:
            initiator_names = InitiatorName.objects.all()
        except:
            raise Http404
        serializer = InitiatorNameSerializer(
            initiator_names, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InitiatorNameDetailAPIView(DestroyModelMixin,
                                 UpdateModelMixin,
                                 generics.RetrieveAPIView):

    def get_object(self, pk):
        try:
            return InitiatorName.objects.get(pk=pk)
        except InitiatorName.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = InitiatorNameSerializer(initiator_name)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        serializer = InitiatorNameSerializer(
            initiator_name, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            initiator_name = self.get_object(pk)
            initiator_name.delete()
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionTypeListView(generics.ListAPIView):
    serializer_class = TransactionTypeSerializer
    queryset = TransactionType.objects.all()

    def list(self, request):
        try:
            transaction_types = TransactionType.objects.all()
        except:
            raise Http404
        serializer = TransactionTypeSerializer(
            transaction_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionTypeDetailAPIView(DestroyModelMixin,
                                   UpdateModelMixin,
                                   generics.RetrieveAPIView):

    def get_object(self, pk):
        try:
            return TransactionType.objects.get(pk=pk)
        except TransactionType.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = TransactionTypeSerializer(transaction_type)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        serializer = TransactionTypeSerializer(
            transaction_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            transaction_type = self.get_object(pk)
            transaction_type.delete()
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerListView(generics.ListAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def list(self, request):
        try:
            customers = Customer.objects.all()
        except:
            raise Http404
        serializer = CustomerSerializer(
            customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerDetailAPIView(DestroyModelMixin,
                            UpdateModelMixin,
                            generics.RetrieveAPIView):

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        serializer = CustomerSerializer(
            customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            customer = self.get_object(pk)
            customer.delete()
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


class IdentifierTypeListView(generics.ListAPIView):
    serializer_class = IdentifierTypeSerializer
    queryset = IdentifierType.objects.all()

    def list(self, request):
        try:
            identifier_types = IdentifierType.objects.all()
        except:
            raise Http404
        serializer = IdentifierTypeSerializer(
            identifier_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IdentifierTypeDetailAPIView(DestroyModelMixin,
                                  UpdateModelMixin,
                                  generics.RetrieveAPIView):

    def get_object(self, pk):
        try:
            return IdentifierType.objects.get(pk=pk)
        except IdentifierType.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = IdentifierSerializer(identifier_type)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        serializer = IdentifierTypeSerializer(
            identifier_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            identifier_type = self.get_object(pk)
            identifier_type.delete()
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def list(self, request):
        try:
            transactions = Transaction.objects.all()
        except:
            raise Http404
        serializer = TransactionSerializer(
            transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionDetailAPIView(UpdateModelMixin,
                               generics.RetrieveAPIView):

    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)


class TransactionResponseListView(generics.ListAPIView):
    serializer_class = TransactionResponseSerializer
    queryset = TransactionResponse.objects.all()

    def list(self, request):
        try:
            transaction_responses = TransactionResponse.objects.all()
        except:
            raise Http404
        serializer = TransactionResponseSerializer(
            transaction_responses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionResponseDetailAPIView(UpdateModelMixin,
                                       generics.RetrieveAPIView):

    def get_object(self, pk):
        try:
            return TransactionResponse.objects.get(pk=pk)
        except TransactionResponse.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = TransactionResponseSerializer(transactionresponse)
        return Response(serializer.data)


class RegistrationListView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    queryset = Registration.objects.all()

    def list(self, request):
        try:
            registrations = Registration.objects.all()
        except:
            raise Http404
        serializer = RegistrationSerializer(
            registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationDetailAPIView(UpdateModelMixin,
                                generics.RetrieveAPIView):

    def get_object(self, pk):
        try:
            return Registration.objects.get(pk=pk)
        except Registration.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = RegistrationSerializer(registration)
        return Response(serializer.data)
