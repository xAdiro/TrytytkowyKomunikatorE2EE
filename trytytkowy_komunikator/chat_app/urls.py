from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.login_page),
    path("logout/", views.logout_action),
    path("register/", views.register_page),
    path("send-message/", views.send_message),
    path("add-friend/", views.send_friend_request),
    path("", views.chat)
]
