from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import MailingCreateView, ClientCreateView, ClientListView, \
    ClientUpdateView, ClientDeleteView, MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    MailingListView, MailingUpdateView, MailingDeleteView, MailingDetailView, toggle_mailing_activity, LogListView, home

app_name = MailingConfig.name

urlpatterns = [
    path('', cache_page(60)(home), name='home'),

    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('update_mailing/<int:pk>/', MailingUpdateView.as_view(), name='update_mailing'),
    path('delete_mailing/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),
    path('mailing_detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('launch_mailing/<int:pk>/', toggle_mailing_activity, name='launch_mailing'),

    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('update_client/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('delete_client/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),

    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('update_message/<int:pk>/', MessageUpdateView.as_view(), name='update_message'),
    path('delete_message/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),

    path('log_list/', LogListView.as_view(), name='log_list'),
]
