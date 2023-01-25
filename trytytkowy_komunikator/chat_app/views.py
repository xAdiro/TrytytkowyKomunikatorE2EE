from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm


def chat(request):
    if not request.user.is_authenticated:
        return redirect("/chat/login/")

    return HttpResponse(f"Hello wordl! {request.user.username}")


def login_page(request):
    if request.method == "POST":
        name = request.POST["login"]
        password = request.POST["password"]
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect("/chat/app/")
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
            return redirect("/chat/app/")

        messages.add_message(request, messages.ERROR, form.error_messages)
        return render(request, "register.html")

    else:
        return render(request, "register.html", {"form": UserCreationForm(request.POST)})


def logout_action(request):
    logout(request)
    return redirect("/chat/login/")


