from django.db import models
from mpesa.models import *
# Create your models here.


class PayCredits(models.Model):
    cashcredit = models.DecimalField(null=True, decimal_places=2, max_digits=6)
    benefactor = models.ForeignKey(Customer,
                                   related_name='PayCredits', null=True)

    class Meta:
        verbose_name = 'PayCredits'
        verbose_name_plural = 'PayCredits'
