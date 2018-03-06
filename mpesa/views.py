import requests
from rest_framework import status
from rest_framework.decorators import *
from rest_framework.renderers import *
from rest_framework.response import Response
import json
# To authenticate your app and get an OAuth access token, use this code.
# An access token expires in 3600 seconds or 1 hour


from requests.auth import HTTPBasicAuth


@api_view(['GET'])
def authenticate(self, format=None):
    consumer_key = "dJjjF6lieZzA62MRlGnd5YSnBBIxcAE1"
    consumer_secret = "kJZcB2pDoulDOwOu"
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    data = r.json()
    return Response(data, status=status.HTTP_200_OK)
