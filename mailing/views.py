import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import inlineformset_factory, formset_factory, modelformset_factory
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from blog.models import Blog
from mailing.forms import MailingForm, MessageMailingForm, ClientForm
from mailing.models import Mailing, MessageMailing, Client, LogsMailing
from users.models import User


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Класс создания рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            # Отключить поле status
            form.fields["status"].disabled = True
        return form

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailingFormset = inlineformset_factory(Mailing, MessageMailing, form=MessageMailingForm, extra=1,
                                               can_delete=False)
        if self.request.method == 'POST':
            context_data['formset'] = MailingFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MailingFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class MailingListView(LoginRequiredMixin, ListView):
    """Класс отображения рассылок"""
    model = Mailing


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Класс редактирования рассылок"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        '''Проверка на то что бы пользователь не мог редактировать чужие данные'''
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailingFormset = inlineformset_factory(Mailing, MessageMailing, form=MessageMailingForm, extra=1,
                                               can_delete=False)
        if self.request.method == 'POST':
            context_data['formset'] = MailingFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MailingFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Класс удаления рассылок"""
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


def client_form(request):
    if request.method == 'POST':
        email = request.POST['email']
        full_name = request.POST['full_name']
        comment = request.POST['comment']
        Client.objects.create(email=email, full_name=full_name, comment=comment)

    return HttpResponseRedirect(reverse('mailing:create'))


class HomeListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Online-MAILING - это отличный вариант отправки рассылок, который вы бы хотели'
        context['qty_mailing'] = Mailing.objects.filter(owner=self.request.user).count
        context['qty_client'] = Client.objects.all().count
        context['activ_mailing'] = Mailing.objects.filter(Q(status='Создана') | Q(status='Запущена')).count
        context['photo_blog'] = Blog.objects.all()[:3]
        return context
