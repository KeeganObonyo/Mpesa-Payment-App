# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models


class Occassion(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)


class MpesaCommandId(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)


class CompanyShortCodeOrNumber(models.Model):
    name = models.IntegerField(null=True)

    def __str__(self):
        return str(self.name)


class InitiatorName(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)


class TransactionType(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)


class IdentifierType(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)

class Transaction(models.Model):
    transaction_type = models.ForeignKey(
        'TransactionType',
        related_name='type',
        null=True,
        on_delete=models.SET_NULL  # Add the on_delete argument
    )
    command_id = models.ForeignKey(
        'MpesaCommandId',
        related_name='command_id',
        null=True,
        on_delete=models.SET_NULL  # Add the on_delete argument
    )
    identifier_type = models.ForeignKey(
        'IdentifierType',
        related_name='identifier_type',
        null=True,
        on_delete=models.SET_NULL  # Add the on_delete argument
    )
    amount = models.DecimalField(
        null=True,
        decimal_places=2,
        max_digits=6
    )
    party_b = models.ForeignKey(
        'CompanyShortCodeOrNumber',
        related_name='party_b',
        null=True,
        on_delete=models.SET_NULL  # Add the on_delete argument
    )
    initiator_name = models.ForeignKey(
        'InitiatorName',
        related_name='company_name',
        null=True,
        on_delete=models.SET_NULL  # Add the on_delete argument
    )
    party_a = models.ForeignKey(
        'CompanyShortCodeOrNumber',
        related_name='party_a',
        on_delete=models.CASCADE  # Add the on_delete argument
    )
    occasion = models.ForeignKey(
        'Occassion',
        related_name='shortcode',
        on_delete=models.CASCADE  # Add the on_delete argument
    )
    account_reference = models.ForeignKey(
        'MpesaCommandId',
        related_name='account_reference',
        null=True,
        on_delete=models.SET_NULL  # Add the on_delete argument
    )
    created = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.transaction_type)


class TransactionResponse(models.Model):  
    originator_conversation_id = models.CharField(
        max_length=200, null=True, blank=True
    )
    response_description = models.CharField(
        max_length=200, null=True, blank=True
    )
    conversation_id = models.CharField(
        max_length=200, null=True, blank=True
    )
    transaction = models.ForeignKey(
        'Transaction',
        related_name='response',
        null=True,
        on_delete=models.SET_NULL  # Add the on_delete argument
    )
    merchant_request_id = models.CharField(
        max_length=200, null=True, blank=True
    )
    checkout_request_id = models.CharField(
        max_length=200, null=True, blank=True
    )
    response_code = models.CharField(
        max_length=200, null=True, blank=True
    )
    result_description = models.CharField(
        max_length=200, null=True, blank=True
    )
    result_code = models.CharField(
        max_length=200, null=True, blank=True
    )

    def __str__(self):
        return str(self.response_description)


class Registration(models.Model):
    company_code = models.ForeignKey(
        CompanyShortCodeOrNumber,
        related_name='company_short_code_or_number',  # Changed to a more descriptive name
        null=True,
        on_delete=models.SET_NULL  # You can choose the appropriate option for your use case
    )
    company_name = models.ForeignKey(
        InitiatorName,
        related_name='registration',
        null=True,
        on_delete=models.SET_NULL  # Choose the appropriate option
    )
    confirmation_url = models.CharField(max_length=200, null=True, blank=True)
    validation_url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.company_name)
