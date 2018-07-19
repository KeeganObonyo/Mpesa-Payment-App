
from django.db import models


class Occassion(models.Model):
    """
    This Model will represent a class for Occassion.
    :type name: string
    :param name: the name of the occassion
    """
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        """Return an ocassion name."""
        return str(self.name)


class MpesaCommandId(models.Model):
    """
    This Model will represent a class for mpesa command ID.
    :type name: string
    :param name: the name of the mpesa command
    """

    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        """Return a mpesa command ID."""
        return str(self.name)


class CompanyShortCodeOrNumber(models.Model):
    """
    This Model will represent a class for company short code or number.
    :type name: string
    :param name: the name of the company short code or number.
    """
    name = models.IntegerField(null=True)

    def __str__(self):
        """Returns a company short code or number."""
        return str(self.name)


class InitiatorName(models.Model):
    """
    This Model will represent a class for Initiator Name.
    :type name: string
    :param name: the name of the initiator name
    """
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        """Returns an initiator name."""
        return str(self.name)


class TransactionType(models.Model):
    """
    This Model will represent a class for Transaction Type.
    :type name: string
    :param name: the name of the initiator name
    """
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        """Returns transaction type."""
        return str(self.name)


class IdentifierType(models.Model):
    """
    This Model will represent a class for Identifier Type.
    :type name: string
    :param name: the name of the Identifier Type.
    """
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        """Returns an identifier type."""
        return str(self.name)


class Transaction(models.Model):
    """
    This Model will represent a class for Transactions.

    :type transaction_type: string
    :param transaction_type: the type of transaction
    :type command_id: integer
    :param command_id: the command id
    :type identifier_type: integer
    :param identifier_type: the identifier type
    :type amount: decimal
    :param amount: The amount of the transaction.Two decimals fixed point number.
    :type party_b: integer
    :param party_b: the company short code id 
    :type  initiator_name: integer
    :param initiator_name: the initiator id 
    :type  party_a: integer
    :param party_a : the company short code or number id
    :type  occasion: integer
    :param occasion: the occassion id
    :type  account_reference: integer
    :param account_reference: the mpesa command id 
    :type created: datetime
    :param created: auto generated date time after transaction object is created.
    :type transaction_description: string 
    :param  transaction_description: the occassion id
    """
    transaction_type = models.ForeignKey(TransactionType,
                                         related_name='type', null=True)
    command_id = models.ForeignKey(MpesaCommandId,
                                   related_name='command_id', null=True)
    identifier_type = models.ForeignKey(IdentifierType,
                                        related_name='identifier_type', null=True)
    amount = models.DecimalField(null=True, decimal_places=2, max_digits=6)
    party_b = models.ForeignKey(CompanyShortCodeOrNumber,
                                related_name='party_b', null=True)
    initiator_name = models.ForeignKey(InitiatorName,
                                       related_name='company_name', null=True)
    party_a = models.ForeignKey(CompanyShortCodeOrNumber,
                                related_name='party_a')
    occasion = models.ForeignKey(Occassion,
                                 related_name='shortcode')
    account_reference = models.ForeignKey(MpesaCommandId,
                                          related_name='account_reference', null=True)
    created = models.DateTimeField(auto_now_add=True)

    transaction_description = models.CharField(max_length=200, null=True)

    def __str__(self):
        """Returns a transaction type."""
        return str(self.transaction_type)


class TransactionResponse(models.Model):
    """
    This Model will represent a class for Transaction Response.
    
    :type originator_conversation_id: string
    :param originator_conversation_id: the originator conversation identification number.
    
    :type response_description: string
    :param response_description: the response_description.
    
    :type conversation_id: string
    :param conversation_id: the conversation identification number.
    
    :type transaction: integer
    :param transaction: the mpesa transaction id that has taken place.

    :type merchant_request_id: string 
    :param merchant_request_id: the merchant_request id 

    :type checkout_request_idn: string 
    :param checkout_request_id: the checkout request id 

    :type checkout_request_idn: string 
    :param checkout_request_id: the checkout request id 

    :type response_code: string 
    :param response_code: the response code 

    :type result_description: string 
    :param result_description: the response code 

    :type result_code: string 
    :param result_code: the result code

    """
    # A unique numeric code generated by the M-Pesa system of the request.
    originator_conversation_id = models.CharField(
        max_length=200, null=True, blank=True)
    # A response message from the M-Pesa system accompanying the response to a
    # request.
    response_description = models.CharField(
        max_length=200, null=True, blank=True)
    # A unique numeric code generated by the M-Pesa system of the response to
    # a request.
    conversation_id = models.CharField(max_length=200, null=True, blank=True)

    transaction = models.ForeignKey(Transaction,
                                    related_name='response', null=True)
    merchant_request_id = models.CharField(
        max_length=200, null=True, blank=True)
    checkout_request_id = models.CharField(
        max_length=200, null=True, blank=True)
    response_code = models.CharField(max_length=200, null=True, blank=True)
    result_description = models.CharField(
        max_length=200, null=True, blank=True)
    result_code = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        """Returns response description."""
        return str(self.response_description)


class Registration(models.Model):
    company_code = models.ForeignKey(
        CompanyShortCodeOrNumber, related_name='CompanyShortCodeOrNumber',
        null=True)
    company_name = models.ForeignKey(InitiatorName,
                                     related_name='registration', null=True)
    confirmation_url = models.CharField(max_length=200, null=True, blank=True)
    validation_url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        """Returns a company name."""
        return str(self.company_name)
