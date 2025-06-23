# from .views import IndexView, set_affluence, AccountingView, PredictionView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.urls import path, reverse_lazy

urlpatterns = [
    path("home", TemplateView.as_view(template_name="app/home.html"), name="home"),
]
