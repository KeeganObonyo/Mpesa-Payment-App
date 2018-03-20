import requests
from rest_framework import status, generics
from rest_framework.decorators import *
from rest_framework.renderers import *
from rest_framework.response import Response
from .models import *
import json
from django.http import Http404
# from m2rypto import RSA, X509
import base64
# from base64 import b64encode
# To authenticate your app and get an OAuth access token, use this code.
# An access token expires in 3600 seconds or 1 hour


from requests.auth import HTTPBasicAuth


@api_view(['GET'])
def authenticate(self):
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


@api_view(['POST'])
def create_b_to_c_transaction(self, *args, **kwargs):
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
                id=party_a).value('name')
            code_b = CompanyCodeOrNumber.objects.filter(
                id=party_b).value('name')
            name = InitiatorName.objects.filter(
                id=initiator_name).value('name')
            com_id = MpesaCommandId.objects.filter(id=command_id).value('name')
            occ = Occasion.objects.filter(id=occasion).value('name')

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
        transaction_response = TransactionResponse.objects.create(
            transaction_feedback=response_description,
            transaction=transaction,
            originator_conversation_id=originator_conversation_id,
            conversation_id=conversation_id
        )
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(responses, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_b_to_b_transaction(self, *args, **kwargs):
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
                id=command_id).value('name')
            party_a = CompanyCodeOrNumber.objects.filter(
                id=party_a).value('name')
            party_b = CompanyCodeOrNumber.objects.filter(
                id=party_b).value('name')
            name = InitiatorName.objects.filter(
                id=initiator_name).value('name')
            id_type_a = IdentifierType.objects.filte(
                id=identifier_type_a).value('name')
            id_type_b = IdentifierType.objects.filte(
                id=identifier_type_a).value('name')
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
        transaction_response = TransactionResponse.objects.create(
            transaction_feedback=response_description,
            transaction=transaction,
            originator_conversation_id=originator_conversation_id,
            conversation_id=conversation_id
        )
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(responses, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def register_c_2_b_url(self, *args, **kwargs):
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
                initiator_name=name,
                confirmation_url=confirmation_url,
                validation_url=validation_url)
        except:
            raise Http404
            party_b = CompanyCodeOrNumber.objects.filter(
                id=party_b).value('name')

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
        transaction_response = TransactionResponse.objects.create(
            response_description=response_description)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(responses, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def check_account_balance(self, *args, **kwargs):
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
                id=command_id).value('name')
            party_a = CompanyCodeOrNumber.objects.filter(
                id=party_a).value('name')
            name = InitiatorName.objects.filter(
                id=initiator_name).value('name')
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
        transaction_response = TransactionResponse.objects.create(
            response_description=response_description,
            transaction=transaction)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(responses, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def check_transaction_status(self, *args, **kwargs):
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
                id=command_id).value('name')
            party_a = CompanyCodeOrNumber.objects.filter(
                id=party_a).value('name')
            party_b = CompanyCodeOrNumber.objects.filter(
                id=party_b).value('name')
            name = InitiatorName.objects.filter(
                id=initiator_name).value('name')
            occ = Occasion.objects.filter(id=occasion).value('name')
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
        transaction_response = TransactionResponse.objects.create(
            transaction_feedback=response_description,
            transaction=transaction,
            originator_conversation_id=originator_conversation_id,
            conversation_id=conversation_id
        )
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(responses, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def transaction_reversal(self, *args, **kwargs):
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
                id=party_a).value('name')
            code_b = CompanyCodeOrNumber.objects.filter(
                id=party_b).value('name')
            name = InitiatorName.objects.filter(
                id=initiator_name).value('name')
            com_id = MpesaCommandId.objects.filter(id=command_id).value('name')

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
        transaction_response = TransactionResponse.objects.create(
            transaction_feedback=response_description,
            transaction=transaction,
            originator_conversation_id=originator_conversation_id,
            conversation_id=conversation_id
        )
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(responses, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_occasion(self, *args, **kwargs):
    occasion = Occasion.objects.create(name=request.data['occasions'])
    return Response(responses, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_mpesa_command_id(self, *args, **kwargs):
    name = MpesaCommandId.objects.create(name=request.data['command_id'])
    return Response(responses, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_company_short_code_or_number(self, *args, **kwargs):
    name = CompanyShortCode.objects.create(
        name=request.data['short_code'])
    return Response(responses, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_initiator_name(self, *args, **kwargs):
    name = InitiatorName.objects.create(
        name=request.data['initiator_name'])
    return Response(responses, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_transaction_type(self, *args, **kwargs):
    name = TransactionType.objects.create(
        name=request.data['transaction_type'])
    return Response(responses, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_customer_name(self, *args, **kwargs):
    name = CustomerName.objects.create(
        name=request.data['transaction_type'])
    return Response(responses, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_identifier_type(self, *args, **kwargs):
    name = IdentifierType.objects.create(
        name=request.data['transaction_type'])
    return Response(response, status=status.HTTP_201_CREATED)


# class OccasionListView(generics.ListAPIView):
#     serializer_class = OccasionSerializer
#     queryset = Occasion.objects.all()

#     def list(self, request):
#         try:
#             occasions = Occasion.objects.all()
#         except:
#             raise Http404
#         serializer = OccasionSerializer(
#             occasions, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class MpesaCommandIdListView(generics.ListAPIView):
#     serializer_class = MpesaCommandIdSerializer
#     queryset = MpesaCommandId.objects.all()

#     def list(self, request):
#         try:
#             command_ids = MpesaCommandId.objects.all()
#         except:
#             raise Http404
#         serializer = MpesaCommandIderializer(
#             command_ids, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
