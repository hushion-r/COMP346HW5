from django.conf.urls import re_path, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='messenger/login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    re_path(r'^signup/$', views.signup, name='signup'),

    re_path(r'message_create', views.message_create, name='message_create'),
    re_path(r'message_save', views.message_save, name='message_save'),
    re_path(r'message_edit', views.message_edit, name='message_edit'),
    re_path(r'^message_update/(?P<message_id>[0-9]+)/$', views.message_update, name='message_update'),

    re_path(r'sent', views.sent, name='sent'),
    re_path(r'inbox', views.inbox, name='inbox'),
    re_path(r'drafts', views.drafts, name='drafts')
]
