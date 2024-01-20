from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, client_form, \
    HomeListView

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('list', MailingListView.as_view(), name='mailing_list'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='delete'),

    path('client_form', client_form, name='client_form'),

]
# handler_404 =
