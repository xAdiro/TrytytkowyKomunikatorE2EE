from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.login_page),
    path("register/", views.register_page),
    path("send-message/", views.send_message),
    path("", views.chat)
]
