import random

from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm, UserAuthenticationForm
from users.models import User
from users.services import send_verify_email_message


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verify')

    def form_valid(self, form):
        user: User = form.save()
        send_verify_email_message(verification_url=self.get_verify_email_url(user), recipient_email=user.email)
        messages.info(self.request, 'Подтвердите почту, чтобы завершить регистрацию')
        return redirect('users:login')

    def get_verify_email_url(self, user) -> str:
        current_site = get_current_site(self.request)
        domain = current_site.domain
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url_path = reverse('users:verify_email', kwargs={'uidb64': uid, 'token': token})
        return f'http://{domain}{url_path}'


class EmailVerify(View):
    def get(self, request: HttpRequest, uidb64: str, token: str):
        user = self.get_user(uidb64)
        if not user or not default_token_generator.check_token(user, token):
            messages.warning(self.request, 'Invalid reset link, please try to get it again')
        else:
            messages.success(self.request, 'Email successfully confirmed')
            user.is_active = True
            user.save()
        return redirect('users:login')

    def get_user(self, uid_base64: str) -> User | None:
        try:
            uid = urlsafe_base64_decode(uid_base64).decode()
            user_id = int(uid)
            user = User.objects.get(pk=user_id)
        except (ValueError, User.DoesNotExist):
            user = None
        return user


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class AuthView(LoginView):
    model = User
    form_class = UserAuthenticationForm


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])

    send_mail(
        "Смена пароля",
        f"Ваш новый пароль: {new_password}",
        settings.EMAIL_HOST_USER,
        [request.user.email],
        fail_silently=False,
    )

    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('users:login'))


class UserListView(ListView):
    model = User


def toggle_activity(request, pk):
    student_item = get_object_or_404(User, pk=pk)

    if student_item.is_active:
        student_item.is_active = False
    else:
        student_item.is_active = True

    student_item.save()

    return redirect(reverse('users:user_list'))
