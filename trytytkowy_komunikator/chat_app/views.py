from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Q

from . import models
from . import forms


def chat(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    return render(request, "chat.html")


def chatbox(request):
    if request.method == "GET":
        converser_username = request.GET["converser"]
        converser_user = User.objects.get(username=converser_username)
        user = User.objects.get(username=request.user)
        key = models.Key.objects.get(owner=user.id)
        converser_key = models.Key.objects.get(owner=converser_user.id)

        # messages--------------------------------
        messages = models.Message.objects.filter(
            Q(receiver=user.id, author=converser_user.id, used_key=key.id)
            | Q(receiver=converser_user.id, author=user.id, used_key=key.id)
        ).order_by("-timestamp")

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
            if request.user.username == author.username:
                is_author.append(True)
                conversation_name.append(receiver)

            else:
                is_author.append(False)
                conversation_name.append(author)

        messages_list = zip(conversation_name, is_author, messages_timestamp, messages_content)

        return render(request, "chatbox_content.html", {
            "messages": messages_list,
            "converser": converser_username,
            "converser_pub_key": converser_key.content
        })


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
        form = forms.NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")

        return render(request, "register.html", {"form": forms.NewUserForm(request.POST)})

    else:
        return render(request, "register.html", {"form": forms.NewUserForm(request.POST)})


def logout_action(request):
    logout(request)
    return redirect("/login/")


def change_password_page(request):
    return render(request, "change_password.html",{"form": PasswordChangeForm(request.POST)})


def friend_requests(request):
    friend_requests_list = [User.objects.get(id=query_id["sender"])
                            for query_id in
                            models.FriendRequest.objects.only("sender").filter(receiver=request.user.id).values(
                                "sender")]

    return render(request, "friend_requests.html", {
        "friend_requests": friend_requests_list
    })


def contacts(request):
    contacts1 = [str(User.objects.get(id=query_id["user2"]))
                 for query_id in
                 models.FriendsWith.objects.filter(user1=request.user.id).values("user2")]

    contacts2 = [str(User.objects.get(id=query_id["user1"]))
                 for query_id in
                 models.FriendsWith.objects.filter(user2=request.user.id).values("user1")]

    contacts1.extend(contacts2)

    return render(request, "contacts.html", {"contacts": contacts1})
