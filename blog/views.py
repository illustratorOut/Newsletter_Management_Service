from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from blog.forms import BlogForm
from blog.models import Blog


class BlogListView(ListView):
    model = Blog


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title1'] = 'Создание контента для блога'
        return context

    def form_valid(self, form):
        self.object = form.save()
        if self.request.user.is_authenticated:
            self.object.owner = self.request.user
            self.object.save()
        return super().form_valid(form)
