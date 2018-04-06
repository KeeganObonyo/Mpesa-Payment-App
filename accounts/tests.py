from django.test import TestCase, RequestFactory
import random
from django.core.urlresolvers import reverse
# Create your tests here.
from django.contrib.auth.models import User

# curl -X POST -H "Content-Type: application/json" -d
# '{"username":"sam","password":"200mg","email":"dude@dude.com","email2":"dude@dude.com","state":"TX","city":"Austin","zip_code":"79424","birthday":"12/23/17","street":"Panadol","ssn":"Panadol",
# "gender":1}' 'http://127.0.0.1:8000/api/accounts/patient/add/'
from .models import *
from .views import *
