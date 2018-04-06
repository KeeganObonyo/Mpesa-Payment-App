from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from rest_framework.views import APIView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)
from .models import (EmergencyContact, Sex,
                     MaritalStatus, Employment,
                     IdentificationType, Address,
                     PhoneNumber, Ethnicity,
                     BloodType, Relationship, Bio)

from django.shortcuts import get_object_or_404
from .serializers import *
from django.contrib.auth import get_user_model
User = get_user_model()


class LoginRequiredMixin(object):
    permission_classes = (permissions.DjangoObjectPermissions,)

    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserListAPIView(ListAPIView):
    #permission_classes = (permissions.DjangoObjectPermissions,)
    serializer_class = UserSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = User.objects.all().order_by('first_name')
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(username__icontains=query)
            ).distinct()
        return queryset_list


class UserDetailAPIView(LoginRequiredMixin,
                        DestroyModelMixin,
                        UpdateModelMixin,
                        generics.RetrieveAPIView):
    permission_classes = (permissions.DjangoObjectPermissions,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        serializer = UserDetailSerializer(
            user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            user = self.get_object(pk)
            user.delete()
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


class GroupCreateAPIView(CreateAPIView):
    #permission_classes = (permissions.DjangoObjectPermissions,)
    serializer_class = GroupCreateSerializer
    queryset = Group.objects.all()


class GroupListAPIView(ListAPIView):
    #permission_classes = (permissions.DjangoObjectPermissions,)
    serializer_class = GroupListSerializer
    queryset = Group.objects.all()


class GroupDetailAPIView(DestroyModelMixin,
                         UpdateModelMixin,
                         generics.RetrieveAPIView):
    permission_classes = (permissions.DjangoObjectPermissions,)

    def get_object(self, pk):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = GroupDetailSerializer(diagnosis)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        serializer = GroupDetailSerializer(
            group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            group = self.get_object(pk)
            group.delete()
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


class BioCreateAPIView(CreateAPIView):
    permission_classes = (permissions.DjangoObjectPermissions,)
    serializer_class = BioCreateSerializer

    def post(self, request, format=None):
        try:
            user = User.objects.get(id=request.data['user'])
        except:
            return Response(status=HTTP_400_BAD_REQUEST)
        address = Address.objects.create()

        em_contact = EmergencyContact.objects.create(
            request.data['em_contact'])
        marital_status = MaritalStatus.objects.create(
            request.data['marital_status'])
        employment = Employment.objects.create(request.data['employment'])
        em_c_relationship = Relationship.objects.create(
            request.data['em_c_relationship'])
        gender = Sex.objects.create(['gender'])
        id_type = IdentificationType.objects.create(request.data['id_type'])
        ethnicity = Ethnicity.objects.create(request.data['ethnicity'])
        blood_type = BloodType.objects.create(request.data['blood_type'])
        bio = Bio.objects.create(user=user,
                                 address=address,
                                 gender=gender,
                                 notes=request.data['notes'],
                                 em_contact=em_contact,
                                 em_c_relationship=em_c_relationship,
                                 main_id_type_no=request.data[
                                     'main_id_type_no'],
                                 birthday=request.data['birthday'],
                                 marital_status=marital_status,
                                 employment=employment,
                                 phone_number=request.data['phone_number'],
                                 id_type=id_type,
                                 ethnicity=ethnicity,
                                 blood_type=blood_type,
                                 preferred_language=request.data[
                                     'preferred_language'],
                                 religion=request.data['religion'])
        return Response(status=HTTP_201_CREATED)


class BioListAPIView(LoginRequiredMixin, ListAPIView):
    permission_classes = (permissions.DjangoObjectPermissions,)
    serializer_class = BioListSerializer
    queryset = Bio.objects.all()


class BioDetailAPIView(LoginRequiredMixin,
                       DestroyModelMixin,
                       UpdateModelMixin,
                       generics.RetrieveAPIView):
    permission_classes = (permissions.DjangoObjectPermissions,)

    def get_object(self, pk):
        try:
            return Bio.objects.get(pk=pk)
        except Bio.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = BioDetailSerializer(bio)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        serializer = BioDetailSerializer(
            bio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            bio = self.get_object(pk)
            bio.delete()
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
