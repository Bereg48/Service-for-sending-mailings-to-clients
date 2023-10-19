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


class HomeView(TemplateView):
    """Представление главной страницы сервиса"""
    extra_context = {
        'title': 'SkyBlog'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_posts = list(Blog.objects.all())
        context['random_post'] = sample(all_posts, min(3, len(all_posts)))
        context['count_mailing'] = get_count_mailing()
        context['active_mailing'] = get_active_mailing()
        context['unique_clients'] = get_unique_clients()

        return context


############################-Mailing-#################################

class MailingListView(LoginRequiredMixin, ListView):
    """Представление для просмотра рассылок"""
    model = Mailing
    form_class = MailingForm
    extra_context = {'title': 'Рассылки'}

    def get_queryset(self):
        """Функция, позволяющая просматривать только свои рассылки для пользователя, который не является менеджером"""
        user = self.request.user
        if user.is_superuser or user.is_staff:
            queryset = Mailing.objects.all()
        else:
            queryset = Mailing.objects.filter(user=user)

        queryset = queryset.filter(is_published=True)
        return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_queryset(self):
        user = self.request.user
        mailing = Mailing.objects.all()
        if user.is_staff or user.is_superuser:
            queryset = mailing
        else:
            queryset = mailing.client.filter(user=user)
        return queryset

    def form_valid(self, form):
        """Если форма валидна, то при создании рассылки запускается периодическая задача и изменяется статус рассылки"""
        mailing = form.save(commit=False)
        mailing.user = self.request.user
        mailing.status = 'CREATE'
        mailing.save()

        message_service = MessageService(mailing)
        send_mailing(mailing)
        message_service.create_task()
        mailing.status = 'START'
        mailing.save()

        return super(MailingCreateView, self).form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для изменения рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления рассылки"""
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


def toggle_status(request, pk):
    """Функция, позволяющая отключать и активировать рассылку"""
    mailing = get_object_or_404(Mailing, pk=pk)
    message_service = MessageService(mailing)
    if mailing.status == 'START' or mailing.status == 'CREATE':
        delete_task(mailing)
        mailing.status = 'FINISH'
    else:
        message_service.create_task()
        mailing.status = 'START'

    mailing.save()

    return redirect(reverse('mailing:mailing_list'))


############################-Message-#################################


# class MessageListView(LoginRequiredMixin, ListView):
#     """Представление для просмотра сообщений"""
#     model = Message
#     form_class = MessageForm
#     extra_context = {'title': 'Сообщения'}
#
#     def get_queryset(self):
#         """Функция, позволяющая просматривать только свои сообщения для пользователя, который не является менеджером"""
#         user = self.request.user
#         if user.is_superuser or user.is_staff:
#             queryset = Message.objects.all()
#         else:
#             queryset = Message.objects.filter(user=user)
#
#         queryset = queryset.filter(is_published=True)
#         return queryset
#
#
# class MessageDetailView(LoginRequiredMixin, DetailView):
#     """Представление для просмотра конкретного сообщения"""
#     model = Message
#
#
# # class MessageCreateView(LoginRequiredMixin, CreateView):
# #     """Представление для создания сообщения"""
# #     model = Message
# #     form_class = MessageForm
# #     success_url = reverse_lazy('message:message_list')
#
# class MessageCreateView(LoginRequiredMixin, CreateView):
#     """Представление для создания сообщения"""
#     model = Message
#     fields = ('header', 'body', 'user')
#     success_url = reverse_lazy('message:message_list')
#
#     # def __init__(self, **kwargs):
#     #     super().__init__(**kwargs)
#     #     self.object = None
#
#
# class MessageUpdateView(LoginRequiredMixin, UpdateView):
#     """Представление для изменения сообщения"""
#     model = Message
#     form_class = MessageForm
#     success_url = reverse_lazy('message:message_list')
#
#
# class MessageDeleteView(LoginRequiredMixin, DeleteView):
#     """Представление для удаления сообщения"""
#     model = Message
#     success_url = reverse_lazy('message:message_list')


############################-Client-#################################

class ClientListView(LoginRequiredMixin, ListView):
    """Представление для просмотра клиентов"""
    model = Client
    extra_context = {'title': 'Клиенты'}

    def get_queryset(self):
        """Функция, позволяющая просматривать только своих клиентов для пользователя, который не является менеджером"""
        user = self.request.user
        if user.is_staff or user.is_superuser:
            queryset = Client.objects.all()
        else:
            queryset = Client.objects.filter(user=user)

        queryset = queryset.filter(is_active=True)
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Представление для просмотра конкретного клиента"""
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        client = form.save(commit=False)
        client.user = self.request.user
        client.save()
        return super(ClientCreateView, self).form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для изменения клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Представление для удаления клиента"""
    model = Client
    success_url = reverse_lazy('mailing:client_list')
    permission_required = 'mailing.delete_client'


############################-MailingLogs-#################################

class MailingLogListView(LoginRequiredMixin, ListView):
    """Представление для просмотра всех попыток рассылок"""
    model = MailingLogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Попытки рассылки"
        context['log_list'] = MailingLogs.objects.all()
        return context
