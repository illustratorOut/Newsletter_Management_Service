import datetime

from django import forms
from django.forms import widgets

from mailing.models import Mailing, MessageMailing, Client


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'
        # exclude = ('сlient',)

        widgets = {
            'time_mailing': forms.TimeInput(
                attrs={'type': 'time',
                       # 'min': datetime.datetime.today().strftime('%H:%M'),
                       'value': datetime.datetime.today().strftime('%H:%M')}),

            'end_datatime_mailing': forms.DateInput(
                format='%Y-%m-%d %H:%M',
                attrs={'type': 'datetime-local',
                       'min': f'{datetime.datetime.today().strftime("%Y-%m-%d")}T{datetime.datetime.today().strftime("%H:%M")}',
                       'value': f'{datetime.datetime.today().strftime("%Y-%m-%d")}T{datetime.datetime.today().strftime("%H:%M")}'
                       }),

        }


class MessageMailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MessageMailing
        fields = '__all__'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
