from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser
)
from datetime import date


class EmergencyContact(models.Model):
    first_name = models.CharField(max_length=200, db_index=True, blank=True)
    last_name = models.CharField(max_length=200, db_index=True, blank=True)
    phone_number = models.CharField(max_length=200, db_index=True, blank=True)
    email = models.CharField(max_length=200, db_index=True, blank=True)
    location = models.CharField(max_length=200, db_index=True, blank=True)


class Sex(models.Model):
    name = models.CharField(max_length=200, db_index=True, blank=True)

    def __unicode__(self):
        return self.name


class MaritalStatus(models.Model):
    name = models.CharField(max_length=200, db_index=True, blank=True)

    def __unicode__(self):
        return self.name


class Employment(models.Model):
    """self employed, unemployed etc"""
    description = models.CharField(max_length=200, db_index=True, blank=True)

    def __str__(self):
        return self.description


class IdentificationType(models.Model):
    """birth certificate no., baptisim card no, passport, national_id etc"""
    name = models.CharField(max_length=10)


class Address(models.Model):
    street = models.CharField(max_length=60, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    # foreignfield for django_country
    country = models.CharField(max_length=20, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)


class PhoneNumber(models.Model):
    phone = models.IntegerField(db_index=True, blank=True)

    def __unicode__(self):
        return self.name


class User(AbstractUser):
    additional_info = models.CharField(max_length=100, null=True, blank=True)
    provider = models.ManyToManyField('self', related_name='rel_doc')

    def __str__(self):
        return "%s %s (%s)" % (self.first_name,
                               self.last_name,
                               self.username)


class Ethnicity(models.Model):
    name = models.CharField(max_length=15)


class BloodType(models.Model):
    name = models.CharField(max_length=15)


class Relationship(models.Model):
    name = models.CharField(max_length=200, db_index=True, blank=True)

    def __str__(self):
        return self.name


class Bio(models.Model):
    marital_status = models.ForeignKey(MaritalStatus, blank=True, null=True)
    employment = models.ForeignKey(Employment, blank=True, null=True)
    user = models.OneToOneField(User, blank=True, null=True)
    id_type = models.ForeignKey(IdentificationType, null=True, blank=True)
    main_id_type_no = models.CharField(max_length=50, null=True, blank=True)
    birthday = models.DateField(default=date.today, blank=True, null=True)
    siblings = models.CharField(max_length=20, blank=True, null=True)
    no_in_household = models.CharField(max_length=20, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    ethnicity = models.ForeignKey(Ethnicity, null=True, blank=True)
    blood_type = models.ForeignKey(BloodType, null=True, blank=True)
    preferred_language = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    notes = models.CharField(max_length=200, db_index=True, blank=True)
    gender = models.ForeignKey(Sex)
    em_contact = models.ForeignKey(EmergencyContact, null=True, blank=True)
    em_c_relationship = models.ForeignKey(Relationship, null=True, blank=True)
    address = models.ForeignKey(Address, null=True, blank=True)
    # include django countries app
