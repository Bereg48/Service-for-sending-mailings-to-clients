from random import sample

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, TemplateView

from blog.models import Blog
from mailing.forms import ClientForm, MailingForm, MessageForm
from mailing.models import *
from mailing.services.services import MessageService, delete_task, send_mailing, get_count_mailing, get_active_mailing, \
    get_unique_clients
from message.models import Message


class MessageListView(LoginRequiredMixin, ListView):
    """Представление для просмотра сообщений"""
    model = Message
    form_class = MessageForm
    extra_context = {'title': 'Сообщения'}

    def get_queryset(self):
        """Функция, позволяющая просматривать только свои сообщения для пользователя, который не является менеджером"""
        user = self.request.user
        if user.is_superuser or user.is_staff:
            queryset = Message.objects.all()
        else:
            queryset = Message.objects.filter(user=user)

        queryset = queryset.filter(is_published=True)
        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Представление для просмотра конкретного сообщения"""
    model = Message


# class MessageCreateView(LoginRequiredMixin, CreateView):
#     """Представление для создания сообщения"""
#     model = Message
#     form_class = MessageForm
#     success_url = reverse_lazy('message:message_list')

class MessageCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания сообщения"""
    model = Message
    fields = ('header', 'body', 'user')
    success_url = reverse_lazy('message:message_list')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для изменения сообщения"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления сообщения"""
    model = Message
    success_url = reverse_lazy('message:message_list')
