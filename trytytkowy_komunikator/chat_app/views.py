from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models


def chat(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    return render(request, "chat.html")


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


