from django.contrib.contenttypes.models import ContentType
from .models import (EmergencyContact, Sex,
                     MaritalStatus, Employment,
                     IdentificationType, Address,
                     PhoneNumber, Ethnicity,
                     BloodType, Relationship, Bio)
from django.contrib.auth.models import Group
from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
    # email2 = EmailField(label='Confirm Email')

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            # 'email2',
            'password',

        ]
        extra_kwargs = {"password":
                        {"write_only": True}
                        }

    def validate(self, data):
        # email = data['email']
        # user_qs = User.objects.filter(email=email)
        # if user_qs.exists():
        #     raise ValidationError("This user has already registered.")
        return data

    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email1")
        # email2 = value
        # if email1 != email2:
        #     raise ValidationError("Emails must match.")

        user_qs = User.objects.filter(email=email1)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")

        return value

    # def validate_email2(self, value):
    #     data = self.get_initial()
    #     email1 = data.get("email")
    #     email2 = value
    #     if email1 != email2:
    #         raise ValidationError("Emails must match.")
    #     return value

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']

        user_obj = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    #username = CharField()
    email = EmailField(label='Email Address')

    class Meta:
        model = User
        fields = [
            # 'username',
            'email',
            'password',
            'token',

        ]
        extra_kwargs = {"password":
                        {"write_only": True}
                        }

    def validate(self, data):
        # email = data['email']
        # user_qs = User.objects.filter(email=email)
        # if user_qs.exists():
        #     raise ValidationError("This user has already registered.")
        return data


class GroupCreateSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class GroupListSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class GroupDetailSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class SexSerializer(ModelSerializer):

    class Meta:
        model = Sex
        fields = '__all__'


class MaritalStatusSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = MaritalStatus
        fields = '__all__'


class EmploymentSerializer(ModelSerializer):

    class Meta:
        model = Employment
        fields = '__all__'


class RelationshipSerializer(ModelSerializer):

    class Meta:
        model = Relationship
        fields = '__all__'


class EmergencyContactSerializer(ModelSerializer):

    class Meta:
        model = EmergencyContact
        fields = '__all__'


class IdentificationTypeSerializer(ModelSerializer):

    class Meta:
        model = IdentificationType
        fields = '__all__'


class AddressSerializer(ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class PhoneNumberSerializer(ModelSerializer):

    class Meta:
        model = PhoneNumber
        fields = '__all__'


class BloodTypeSerializer(ModelSerializer):

    class Meta:
        model = BloodType
        fields = '__all__'


class EthnicitySerializer(ModelSerializer):

    class Meta:
        model = Ethnicity
        fields = '__all__'


class BioDetailSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Bio
        fields = '__all__'


class BioCreateSerializer(ModelSerializer):
    address = AddressSerializer()
    em_contact = EmergencyContactSerializer()
    em_c_relationship = RelationshipSerializer()
    marital_status = MaritalStatusSerializer()
    id_type = IdentificationTypeSerializer()
    ethnicity = EthnicitySerializer()
    gender = SexSerializer()
    employment = EmploymentSerializer()
    blood_type = BloodTypeSerializer()

    class Meta:
        model = Bio
        fields = '__all__'
        extra_kwargs = {"ssn":
                        {"write_only": True}
                        }

    def create(self, validated_data):
        return Bio.objects.create(**validated_data)


class BioListSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Bio
        fields = '__all__'
