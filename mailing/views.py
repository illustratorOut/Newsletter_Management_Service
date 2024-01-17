from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingForm, MessageMailingForm, ClientForm
from mailing.models import Mailing, MessageMailing, Client


class MailingCreateView(CreateView):
    """Класс создания рассылки"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:mailing_list')

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)
    #     if not self.request.user.is_superuser:
    #         # Отключить поле status
    #         form.fields["status"].disabled = True
    #     return form

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailingFormset = inlineformset_factory(Client, Mailing, form=MailingForm, extra=1,
                                               can_delete=False)
        ClientFormset = inlineformset_factory(Mailing, MessageMailing, form=MessageMailingForm, extra=1,
                                              can_delete=False)
        if self.request.method == 'POST':
            context_data['formset'] = MailingFormset(self.request.POST, instance=self.object)
            context_data['formset1'] = ClientFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MailingFormset(instance=self.object)
            context_data['formset1'] = ClientFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class MailingListView(ListView):
    """Класс отображения рассылок"""
    model = Mailing


class MailingUpdateView(UpdateView):
    """Класс редактирования рассылок"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

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
        return super().form_valid(form)


class MailingDeleteView(DeleteView):
    """Класс удаления рассылок"""
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
