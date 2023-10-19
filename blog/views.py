from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from blog.forms import BlogForms
from blog.models import Blog, Contacts


class BlogListView(ListView):
    """Представление для просмотра блогов"""
    model = Blog
    form_class = BlogForms
    success_url = reverse_lazy('blog:blog_list')
    template_name = 'blog/blog_list.html'


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class BlogDetailView(LoginRequiredMixin, DetailView):
    """Представление для просмотра конкретного блога"""
    model = Blog
    form_class = BlogForms
    success_url = reverse_lazy('blog:blog_detail')
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        object = super().get_object(queryset=queryset)
        object.view_count += 1
        object.save()
        return object


class BlogCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания блога"""
    model = Blog
    fields = ('title', 'text', 'image', 'is_active')
    success_url = reverse_lazy('blog:blog_list')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для изменения блога"""
    model = Blog
    fields = ('title', 'text', 'image', 'is_active')

    def get_success_url(self):
        return reverse('mailing:blog_detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления блога"""
    model = Blog
    success_url = reverse_lazy('mailing:blog_list')


class ContactView(TemplateView):
    """Представление страницы контактов сервиса"""
    model = Contacts
