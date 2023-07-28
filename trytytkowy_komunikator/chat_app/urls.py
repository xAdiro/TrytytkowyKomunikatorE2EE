from django.urls import path

import trytytkowy_komunikator.chat_app.actions
from . import views
from . import actions


urlpatterns = [
    path("login/", views.login_page),
    path("logout/", views.logout_action),
    path("register/", views.register_page),
    path("send-message/", trytytkowy_komunikator.chat_app.actions.send_message),
    path("chatbox/", views.chatbox),
    path("add-friend/", trytytkowy_komunikator.chat_app.actions.send_friend_request),
    path("accept-friend-request/", actions.accept_friend_request),
    path("delete-friend-request/", actions.delete_friend_request),
    path("", views.chat),
    path("change-password/", views.change_password_page),
    path("change-password-action/", trytytkowy_komunikator.chat_app.actions.change_password_action),
    path("update-pub-key/", trytytkowy_komunikator.chat_app.actions.update_pub_key),
    path("friend-requests/", views.friend_requests),
    path("delete-friend/", trytytkowy_komunikator.chat_app.actions.delete_friend),
    path("contacts/", views.contacts)
]
