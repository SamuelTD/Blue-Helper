# from .views import IndexView, set_affluence, AccountingView, PredictionView
from django.views.generic import TemplateView
from django.urls import path

urlpatterns = [
    path("home", TemplateView.as_view(template_name="app/home.html"), name="home"),
    path("chat", TemplateView.as_view(template_name="app/chat.html"), name="chat"),
]
