from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.http import HttpResponse
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
            models.FriendsWith(user1=requesting_user, user2=receiving_user).save()

    return redirect("/")


def send_friend_request(request):
    if not request.user.is_authenticated or request.method != "POST":
        return HttpResponse(content="", status=403)

    receiver_username = request.POST.get("username", default="")
    receiver_user = User.objects.get(username=receiver_username)

    if models.FriendRequest.objects.filter(sender=request.user,
                                           receiver=User.objects.get(username=receiver_username)).count() > 0:
        HttpResponse(content="", status=403)

    if models.FriendRequest.objects.filter(sender=receiver_user, receiver=request.user).count() > 0:
        models.FriendRequest.objects.get(sender=receiver_user, receiver=request.user).delete()
        models.FriendsWith(user1=receiver_user, user2=request.user).save()
        HttpResponse(content="", status=403)

    if not _is_friend_with(request.user.username, receiver_username) and request.user.username != receiver_username:
        friend_request = models.FriendRequest(
            sender=User.objects.get(username=request.user.username),
            receiver=User.objects.get(username=receiver_username)
        )
        friend_request.save()

    return HttpResponse(content="", status=201)


def _is_friend_with(username1: str, username2: str) -> bool:
    user1 = User.objects.get(username=username1)
    user2 = User.objects.get(username=username2)

    return models.FriendsWith.objects.filter(user1=user1.id, user2=user2.id).count() >= 1 \
        or models.FriendsWith.objects.filter(user1=user2.id, user2=user1.id).count() >= 1


def change_password_action(request):
    if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                messages.success(request, 'Your password was successfully updated!')
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect("/")
            else:
                messages.error(request, "Please input correct credentials")
                return redirect("/change-password/")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "chat.html")


def delete_friend(request):
    friend_username = request.POST["friend_username"]
    models.FriendsWith.objects.get(
        Q(user1=request.user, user2=User.objects.get(username=friend_username)) |
        Q(user2=request.user, user1=User.objects.get(username=friend_username))
    ).delete()
    return HttpResponse(content="", status=201)


def send_message(request):
    if not request.user.is_authenticated or request.method != "POST":
        return HttpResponse(content="", status=403)

    content = request.POST.get("message", default="")
    receiver_name = request.POST.get("receiver")
    used_key = request.POST.get("used_key")

    message = models.Message(
        author=User.objects.get(username=request.user.username),
        receiver=User.objects.get(username=receiver_name),
        used_key=models.Key.objects.get(content=used_key),
        content=content
    )
    message.save()
    return HttpResponse(content="", status=201)


def update_pub_key(request):
    if request.method == "POST":
        new_key = request.POST["key"]
        user = User.objects.get(username=request.user.username)
        models.Key.objects.filter(owner=user).delete()
        models.Key(owner=user, content=new_key).save()

        return redirect("/")
