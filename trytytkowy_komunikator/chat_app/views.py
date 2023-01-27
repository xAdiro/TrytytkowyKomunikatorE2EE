from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Q

from . import models
from . import forms


def chat(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    # friend requests-------------------------

    user = User.objects.get(username=request.user.username)

    # contacts--------------------------------

    contacts1 = [str(User.objects.get(id=query_id["user2"]))
                 for query_id in
                 models.FriendsWith.objects.filter(user1=user.id).values("user2")]

    contacts2 = [str(User.objects.get(id=query_id["user1"]))
                 for query_id in
                 models.FriendsWith.objects.filter(user2=user.id).values("user1")]

    contacts1.extend(contacts2)

    return render(request, "chat.html", {
        "contacts": contacts1,
    })


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


def send_message(request):
    if not request.user.is_authenticated or request.method != "POST":
        return redirect("/")

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
        form = forms.NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful")
            return redirect("/")

        return render(request, "register.html", {"form": forms.NewUserForm(request.POST)})

    else:
        return render(request, "register.html", {"form": forms.NewUserForm(request.POST)})


def logout_action(request):
    logout(request)
    return redirect("/login/")


def send_friend_request(request):
    if not request.user.is_authenticated or request.method != "POST":
        return redirect("/")

    receiver_username = request.POST.get("username", default="")
    receiver_user = User.objects.get(username=receiver_username)

    if models.FriendRequest.objects.filter(sender=request.user,
                                           receiver=User.objects.get(username=receiver_username)).count() > 0:
        return redirect("/")

    if models.FriendRequest.objects.filter(sender=receiver_user, receiver=request.user).count() > 0:
        models.FriendRequest.objects.get(sender=receiver_user, receiver=request.user).delete()
        models.FriendsWith(user1=receiver_user, user2=request.user).save()
        return redirect("/")

    if not _is_friend_with(request.user.username, receiver_username) and request.user.username != receiver_username:
        friend_request = models.FriendRequest(
            sender=User.objects.get(username=request.user.username),
            receiver=User.objects.get(username=receiver_username)
        )
        friend_request.save()

    return redirect("/")


def update_pub_key(request):
    if request.method == "POST":
        new_key = request.POST["key"]
        user = User.objects.get(username=request.user.username)
        models.Key.objects.filter(owner=user).delete()
        models.Key(owner=user, content=new_key).save()

        return redirect("/")


def _is_friend_with(username1: str, username2: str) -> bool:
    user1 = User.objects.get(username=username1)
    user2 = User.objects.get(username=username2)

    return models.FriendsWith.objects.filter(user1=user1.id, user2=user2.id).count() >= 1 \
        or models.FriendsWith.objects.filter(user1=user2.id, user2=user1.id).count() >= 1



def change_password_page(request):
    return render(request, "change_password.html",{"form": PasswordChangeForm(request.POST)})

def change_password_action(request):
    print("DDDDDDDD")
    if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            print("CCCCCCCC")
            if form.is_valid():
                print("BBBBBBBBBBBB")
                messages.success(request, 'Your password was successfully updated!')
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect("/")
            else:
                print("AAAAAAAAAAAA")
                messages.error(request, "Please correct the error below.")
                return redirect("/change-password/")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "chat.html")


    # if request.method == "POST":
    #     oldpassword = request.POST["old-password"]
    #     newpassword = request.POST["new-password"]
    #     newpassword2 = request.POST["new-password2"]
    #     user = authenticate(request, username=request.user.username, password=oldpassword)
    #     print(user)
    #     if user is None:
    #         messages.add_message(request, messages.ERROR, "Wrong old password")
    #         return redirect("/change-password/")
    #     if newpassword != newpassword2:
    #         messages.add_message(request, messages.ERROR, "Password mismatched")
    #         return redirect("/change-password/")
    #     user.set_password(newpassword)
    #     user.save()
    #     return redirect("/")
    # return redirect("/")


def friend_requests(request):
    friend_requests_list = [User.objects.get(id=query_id["sender"])
                            for query_id in
                            models.FriendRequest.objects.only("sender").filter(receiver=request.user.id).values(
                                "sender")]

    return render(request, "friend_requests.html", {
        "friend_requests": friend_requests_list
    })


def delete_friend(request):
    friend_username = request.POST["friend_username"]
    models.FriendsWith.objects.get(
        Q(user1=request.user, user2=User.objects.get(username=friend_username) |
        Q(user2=request.user, user1=User.objects.get(username=friend_username)))
    ).delete()
    return redirect("/")
