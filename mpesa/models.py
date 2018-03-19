from django.db import models
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Occassion(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)


class MpesaCommandId(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)


class CompanyShortCode(models.Model):
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


class Transaction(models.Model):
    transaction_type = models.ForeignKey(TransactionType,
                                         related_name='type', null=True)
    command_id = models.ForeignKey(MpesaCommandId,
                                   related_name='command_id', null=True)
    amount = models.DecimalField(null=True, decimal_places=2, max_digits=6)
    comments = models.CharField(max_length=200, null=True)
    phoneno = models.IntegerField(null=True)
    initiator_name = models.ForeignKey(InitiatorName,
                                       related_name='company_name', null=True)
    shortcode = models.ForeignKey(CompanyShortCode,
                                  related_name='short_code')
    occasion = models.ForeignKey(Occassion,
                                 related_name='shortcode')

    def __str__(self):
        return str(self.transaction_type)


class TransactionResponse(models.Model):
    transaction_feedbacks = models.CharField(max_length=200, blank=True)
    transaction = models.ForeignKey(Transaction,
                                    related_name='response', null=True)

    def __str__(self):
        return str(self.response)
