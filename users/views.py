from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import EmailMessage, mailers
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object

        login(self.request, user)

        message = EmailMessage(
            subject="Добро пожаловать в Catalog!",
            body=(
                f"Здравствуйте, {user.email}!\n\n"
                "Спасибо за регистрацию в сервисе Catalog.\n"
                "Теперь вы можете просматривать товары и управлять ими."
            ),
            from_email="noreply@catalog.local",
            to=[user.email],
        )

        mailers["default"].send_messages([message])

        return response


class UserLoginView(LoginView):
    template_name = "users/login.html"


class UserLogoutView(LogoutView):
    next_page = "/"


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user