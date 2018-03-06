import requests
from rest_framework import status
from rest_framework.decorators import *
from rest_framework.renderers import *
from rest_framework.response import Response
import json
#from m2rypto import RSA, X509
from base64 import b64encode
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

    return Response(data, status=status.HTTP_200_OK)


INITIATOR_PASS = "YOUR_PASSWORD"
CERTIFICATE_FILE = "PATH_TO_CERTIFICATE_FILE"

# Base64 encoded string of the Security Credential, which is encrypted
# using M-Pesa public key and validates the transaction on M-Pesa Core
# system.


@api_view()
def encryptInitiatorPassword():
    cert_file = open(CERTIFICATE_FILE, 'r')
    cert_data = cert_file.read()  # read certificate file
    cert_file.close()

    cert = X509.load_cert_string(cert_data)
    #pub_key = X509.load_cert_string(cert_data)
    pub_key = cert.get_pubkey()
    rsa_key = pub_key.get_rsa()
    cipher = rsa_key.public_encrypt(INITIATOR_PASS, RSA.pkcs1_padding)
    return b64encode(cipher)


def busines_to_customer_payment(self):

    access_token = "Access-Token"
    api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
    initiator = encryptInitiatorPassword(r)
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "InitiatorName": "XELPHAHEALTH ",
        "SecurityCredential": initiator,
        "CommandID": "BusinessPayment",
        "Amount": " ",
        "PartyA": " ",
        "PartyB": " ",
        "Remarks": " ",
        "QueueTimeOutURL": "/",
        "ResultURL": "mpesa/transactions_record/",
        "Occasion": ""
    }

    response = requests.post(api_url, json=request, headers=headers)

    print(response.text)


@api_view(['POST'])
def transactions_record(self):
    transaction = Transaction.objects.create(
        response=response.data)
    return Response(status=status.HTTP_201_CREATED)
