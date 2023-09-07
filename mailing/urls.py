from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.views import *

urlpatterns = [
    path('', HomeView.as_view(template_name='mailing/home.html'), name='home'),
    # mailing
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/delete/<int:pk>/', cache_page(60)(MailingDeleteView.as_view()), name='mailing_delete'),
    # message
    path('message/', MessageListView.as_view(template_name='mailing/message_list.html'), name='message_list'),
    path('message/detail/<int:pk>/', cache_page(60)(MessageDetailView.as_view()), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(template_name='mailing/message_detail.html'),
         name='message_create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', cache_page(60)(MessageDeleteView.as_view()), name='message_delete'),
    path('toggle/<int:pk>/', toggle_status, name='toggle_status'),
    # clients
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/detail/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='client_detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # mailing_log
    path('mailing_log/', MailingLogListView.as_view(), name='mailing_log_list'),
]
