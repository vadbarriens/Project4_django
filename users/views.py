import secrets

from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(15)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение электронного адреса",
            message=f"Спасибо за регистрацию на нашем сайте. "
            f"Подвердите адрес электронной почты, перейдя по следующей ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect("users:login")


class UserBlockView(View):
    permission_required = "users.can_block_user"

    def post(self, request: HttpRequest, *args: str, **kwargs):
        user = get_object_or_404(User, email=self.kwargs.get("email"))
        if not user.is_active:
            user.is_active = True
            user.save()
            messages.success(self.request, "Пользователь успешно разблокирован!")
        else:
            user.is_active = False
            user.save()
            messages.success(self.request, "Пользователь успешно заблокирован!")
        return redirect("users:users_list")


class UserListView(ListView):
    model = User
    template_name = "users/users_list.html"
    permission_required = "view_user"
    context_object_name = "users"
