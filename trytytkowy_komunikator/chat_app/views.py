from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q

from . import models


def chat(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    #friend requests-------------------------

    user = User.objects.get(username=request.user.username)
    friend_requests = [User.objects.get(id=query_id["sender"])
                       for query_id in
                       models.FriendRequest.objects.only("sender").filter(receiver=user.id).values("sender")]

    #contacts--------------------------------

    contacts1 =[str(User.objects.get(id=query_id["user2"]))
                 for query_id in
                 models.FriendsWith.objects.filter(user1=user.id).values("user2")]

    contacts2 = [str(User.objects.get(id=query_id["user1"]))
                 for query_id in
                 models.FriendsWith.objects.filter(user2=user.id).values("user1")]

    contacts1.extend(contacts2)

    return render(request, "chat.html", {
        "friend_requests": friend_requests,
        "contacts": contacts1,
    })


def chatbox(request):
    if request.method == "GET":
        converser_username = request.GET["converser"]
        converser_user = User.objects.get(username=converser_username)
        user = User.objects.get(username=request.user)

        # messages--------------------------------
        messages = models.Message.objects.filter(
            Q(receiver=user.id, author=converser_user.id) | Q(receiver=converser_user.id, author=user.id)
        ).order_by("timestamp")

        print(messages)
        messages_authors = [User.objects.get(id=query_id["author"])
                            for query_id in
                            messages.values("author")]

        messages_receivers = [User.objects.get(id=query_id["receiver"])
                              for query_id in
                              messages.values("receiver")]

        messages_timestamp = [query_id["timestamp"]
                              for query_id in
                              messages.values("timestamp")]

        messages_content = [query_id["content"]
                            for query_id in
                            messages.values("content")]

        conversation_name = []
        is_author = []

        for author, receiver in zip(messages_authors, messages_receivers):
            if request.user.username == author:
                is_author.append(True)
                conversation_name.append(receiver)

            else:
                is_author.append(False)
                conversation_name.append(author)

        messages_list = zip(conversation_name, is_author, messages_timestamp, messages_content)

        return render(request, "chatbox_content.html", {
            "messages": messages_list,
            "converser": converser_username,
        })


def send_message(request):
    if not request.user.is_authenticated or request.method != "POST":
        return redirect("/")

    content = request.POST.get("message", default="")

    message = models.Message(
        author=User.objects.get(username=request.user.username),
        receiver=User.objects.get(username=request.user.username),
        used_key=models.Key.objects.get(content="abc123"),
        content=content
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
