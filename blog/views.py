from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from blog.forms import BlogForm
from blog.models import Blog


class BlogListView(ListView):
    model = Blog


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:home')
