from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from . import models


def accept_friend_request(request):
    return delete_friend_request(request, add_frienship=True)


def delete_friend_request(request, add_frienship=False):
    if not request.user.is_authenticated or request.method != "POST":
        return redirect("/")

    requester_name = request.POST.get("username")

    receiving_user = User.objects.get(username=request.user.username)
    requesting_user = User.objects.get(username=requester_name)
    friend_request = models.FriendRequest.objects.get(sender=requesting_user, receiver=receiving_user)

    if friend_request is not None:
        friend_request.delete()

        if add_frienship:
            models.FriendsWith(requesting_user, receiving_user).save()

    return redirect("/")


def _friend_request_alredy_received(receiving_user: User, requesting_user: User) -> models.FriendRequest:
    pass
