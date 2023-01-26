from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models


def chat(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    user = User.objects.get(username=request.user.username)
    friend_requests = [User.objects.get(id=query_id["sender"])
                       for query_id in
                       models.FriendRequest.objects.filter(receiver=user.id).values("sender")]

    # messages =
    # contacts =

    contacts1 = [models.FriendsWith.objects.get(id=query_id["user2"])
                       for query_id in
                       models.FriendsWith.objects.filter(user1=user.id).values("user1")]

    contacts2 = [models.FriendsWith.objects.get(id=query_id["user1"])
                       for query_id in
                       models.FriendsWith.objects.filter(user2=user.id).values("user2")]

    contacts1.extend(contacts2)


    return render(request, "chat.html", {
        "friend_requests": friend_requests,
        "contacts": contacts1
    })


def send_message(request):
    if not request.user.is_authenticated or request.method != "POST":
        return redirect("/")

    message_author_content = request.POST.get("message_for_author", default="")
    message_receiver_content = request.POST.get("message_for_receiver", default="")

    message = models.Message(
        author=User.objects.get(username=request.user.username),
        receiver_key=models.Key.objects.get(content="abcdef1234"),
        author_content=message_author_content,
        receiver_content=message_receiver_content
    )
    message.save()
    return redirect("/")


def login_page(request):
    if request.method == "POST":
        name = request.POST["login"]
        password = request.POST["password"]
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.add_message(request, messages.ERROR, "Incorrect username or password")
            return render(request, "login.html")

    else:
        return render(request, "login.html")


def register_page(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful")
            return redirect("/")

        messages.add_message(request, messages.ERROR, form.error_messages)
        return render(request, "register.html")

    else:
        return render(request, "register.html", {"form": UserCreationForm(request.POST)})


def logout_action(request):
    logout(request)
    return redirect("/login/")


def send_friend_request(request):
    if not request.user.is_authenticated or request.method != "POST":
        return redirect("/")

    receiver_username = request.POST.get("username", default="")

    if not _is_friend_with(request.user.username, receiver_username) and request.user.username != receiver_username:
        friend_request = models.FriendRequest(
            sender=User.objects.get(username=request.user.username),
            receiver=User.objects.get(username=receiver_username)
        )
        friend_request.save()

    return redirect("/")


def _is_friend_with(username1: str, username2: str) -> bool:
    user1 = User.objects.get(username=username1)
    user2 = User.objects.get(username=username2)

    return models.FriendsWith.objects.filter(user1=user1.id, user2=user2.id).count() >= 1 \
        or models.FriendsWith.objects.filter(user1=user2.id, user2=user1.id).count() >= 1
