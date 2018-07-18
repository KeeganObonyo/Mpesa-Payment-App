from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)
from rest_framework import serializers
from .models import *


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = '__all__'


class TransactionResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionResponse
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'


class IdentifierTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = IdentifierType
        fields = '__all__'


class OccassionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Occassion
        fields = '__all__'


class TransactionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionType
        fields = '__all__'


class InitiatorNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = InitiatorName
        fields = '__all__'


class CompanyShortCodeOrNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyShortCodeOrNumber
        fields = '__all__'


class MpesaCommandIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = MpesaCommandId
        fields = '__all__'
