from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

from users.apps import UsersConfig
from users.services import is_active_key_registration
from users.views import RegisterView, UsersListView, change_task_status

app_name = UsersConfig.name

urlpatterns = [
    path('login', cache_page(60)(LoginView.as_view(template_name='users/login.html')), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('client', UsersListView.as_view(), name='client'),
    path('key-registration/<str:key>', is_active_key_registration, name='key_registration'),

    path('task-status/<int:pk>/<str:status>/', change_task_status, name='change_task_status'),
]
