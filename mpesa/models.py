from django.db import models
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _

# Create your models here.


"""class MpesaCommandId(model.Models):
    CHOICES = Choices(
        (1, 'TransactionReversal'),  # Reversal
        (2, 'SalaryPayment'),  # employer to employees
        (3, 'BusinessPayment'),  # business to customer
        (4, 'PromotionPayment'),  # money on promotions
        (5, 'AccountBalance'),
        (6, 'CustomerPayBillOnline'),
        # Used to simulate a transaction taking place in the case of C2B
        # Simulate Transaction or to initiate a transaction on behalf of the
        # customer (STK Push).
        (7, 'TransactionStatusQuery'),  # query the details of a transaction.
        (8, 'CheckIdentity'),  # Smlr to STK, M-Pesa PIN as service.
        (9, 'BusinessPayBill'),  # one paybill to another paybill
        (10, 'BusinessBuyGoods'),  # buy goods to another buy goods
        (11, 'DisburseFundsToBusiness'),  # funds from utility to MMF account.
        (12, 'BusinessToBusinessTransfer'),  # MMF 1 2 o paybill MMF account.
        (13, 'BusinessTransferFromMMFToUtilitys'))  # Transferring funds from paybills MMF to another paybills utility account.
    name = models.CharField(max_length=200, choices=CHOICES)

    def __str__(self):
        return str(self.name)

"""


class Transactions(models.Model):
    response = models.CharField(max_length=200, db_index=True, blank=True)

    def __str__(self):
        return str(self.response)
