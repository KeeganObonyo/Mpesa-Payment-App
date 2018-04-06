from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^get_users/$', UserListAPIView.as_view(), name='user_list'),
    url(r'^user/(?P<pk>\d+)/$', UserDetailAPIView.as_view(), name='thread'),
    url(r'^add_group/$', GroupCreateAPIView.as_view(), name='group_add'),
    url(r'^get_group/$', GroupListAPIView.as_view(), name='group_list'),
    url(r'^group/(?P<pk>\d+)/$', GroupDetailAPIView.as_view(), name='thread'),
    url(r'^add_bio/$', BioCreateAPIView.as_view(), name='bio_add'),
    url(r'^get_bio/$', BioListAPIView.as_view(), name='bio_list'),
    url(r'^bio/(?P<pk>\d+)/$', BioDetailAPIView.as_view(), name='thread'),
]
