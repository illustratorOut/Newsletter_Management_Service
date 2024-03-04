import random

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from users.forms import UserRegisterForm, UserForm
from users.models import User
from users.services import get_send_mail


class RegisterView(CreateView):
    """Регистрация пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        while True:
            random_key_registration = ''.join([str(random.randint(0, 9)) for _ in range(12)])
            if form.is_valid():
                if User.objects.filter(registration_key=random_key_registration):
                    continue
                else:
                    new_key = form.save()
                    try:
                        new_key.registration_key = random_key_registration
                        new_key.save()
                        get_send_mail(self.object.email, random_key_registration)
                    except:
                        pass

                    return super().form_valid(form)
        return super().form_valid(form)


class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    form_class = UserForm
    success_url = '/'
    permission_required = 'users.view_user'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     """Если авторизованный пользователь superuser то в списке пользователей удалять строку админа """
    #     context = super().get_context_data(**kwargs)
    #     if not self.request.user.is_superuser:
    #         context['object_list'] = User.objects.filter(is_staff=False).filter(is_superuser=False)
    #     else:
    #         context['object_list'] = User.objects.exclude(email=self.request.user)
    #     return context


def change_task_status(request, pk, status):
    task = User.objects.get(pk=pk)
    task.is_active = status
    task.save()
    return redirect('users:client')
