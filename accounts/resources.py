"""from import_export import resources
from django.contrib.auth.models import User
from .models import *


class UserResource(resources.ModelResource):

    class Meta:
        model = User


class MaritalStatusResource(resources.ModelResource):

    class Meta:
        model = MaritalStatus


class PhoneNumberResource(resources.ModelResource):

    class Meta:
        model = PhoneNumber


class EmploymentResource(resources.ModelResource):

    class Meta:
        model = Employment


class SexResource(resources.ModelResource):

    class Meta:
        model = Sex


class IdentificationTypeResource(resources.ModelResource):

    class Meta:
        model = IdentificationType
"""
