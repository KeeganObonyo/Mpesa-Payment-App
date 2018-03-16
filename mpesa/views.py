import requests
from rest_framework import status
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
def create_transaction(self, *args, **kwargs):
    access_token = authenticate()
    try:
        try:
            shortcode = CompanyShortCode.objects.get(
                id=request.data['company_short_code'])
            initiator_name = InitiatorName.objects.get(
                id=request.data['company_name'])
            transaction_type = TransactionType.objects.get(
                id=request.data['transaction_type'])
            transaction = Transaction.objects.create(
                amount=request.data['amount'],
                comments=request.data['comments'],
                phoneno=request.data['phoneno'],
                shortcode=shortcode,
                transaction_type=transaction_type,
                initiator_name=initiator_name)
        except:
            raise Http404
        api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
#        initiator = encryptInitiatorPassword(r)
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "InitiatorName": company_name,
            "SecurityCredential": initiator,
            "CommandID": "BusinessPayment",
            "Amount": amount,
            "PartyA": shortcode,
            "PartyB": phoneno,
            "Remarks": comments,
            "QueueTimeOutURL": "/",
            "ResultURL": "/",
            "Occasion": ""
        }

        response = requests.post(api_url, json=request, headers=headers)
        transaction_feedback = response['ResponseDescription']
        transaction_response = TransactionResponse.objects.create(
            transaction_feedback=transaction_feedback,
            transaction=transaction
        )
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(responses, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# def transactions_record(self):
#     transaction = Transaction.objects.create(
#         response=response.data)
#     return Response(status=status.HTTP_201_CREATED)
