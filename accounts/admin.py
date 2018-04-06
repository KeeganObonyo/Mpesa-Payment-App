from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from .resources import *
#from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.conf import settings

"""@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource


@admin.register(MaritalStatus)
class MaritalStatusAdmin(ImportExportModelAdmin):
    resource_class = MaritalStatusResource


@admin.register(Telephone)
class PhoneNumberAdmin(ImportExportModelAdmin):
    resource_class = TelephoneResource


@admin.register(Employment)
class EmploymentAdmin(ImportExportModelAdmin):
    resource_class = EmploymentResource


@admin.register(Sex)
class SexAdmin(ImportExportModelAdmin):
    resource_class = SexResource


@admin.register(IdentificationType)
class IdentificationTypeAdmin(ImportExportModelAdmin):
    resource_class = IdentificationTypeResourceadmin.site.register(MaritalStatus)"""

admin.site.register(User)
admin.site.register(Address)
admin.site.register(EmergencyContact)
admin.site.register(MaritalStatus)
admin.site.register(PhoneNumber)
admin.site.register(IdentificationType)
