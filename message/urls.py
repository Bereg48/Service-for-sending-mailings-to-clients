from django.urls import path
from django.views.decorators.cache import cache_page


from mailing.views import *
from message.apps import MessageConfig
from message.views import MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView
app_name = MessageConfig.name

urlpatterns = [

    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/detail/<int:pk>/', cache_page(60)(MessageDetailView.as_view()), name='message_detail'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', cache_page(60)(MessageDeleteView.as_view()), name='message_delete'),

]