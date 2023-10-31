from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, AuthView, ProfileView, EmailVerify, generate_new_password, UserListView, \
    toggle_activity

app_name = UsersConfig.name

urlpatterns = [
    path('', AuthView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity')
]
