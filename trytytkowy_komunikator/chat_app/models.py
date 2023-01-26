from django.db.models import Model, CharField, DateField, DateTimeField, TextField, ForeignKey, CASCADE, SET_NULL
from django.contrib.auth.models import User
from django.forms import ModelForm


class Key(Model):
    content = CharField(max_length=100)
    last_used = DateField(auto_now_add=True)


class KeyUser(User):
    current_key = ForeignKey(Key, on_delete=SET_NULL, null=True)


class Message(Model):
    author = ForeignKey(User, on_delete=CASCADE, related_name="%(class)s_author")
    receiver = ForeignKey(User, on_delete=CASCADE, related_name="%(class)s_receiver")

    used_key = ForeignKey(Key, on_delete=CASCADE)

    content = TextField()
    timestamp = DateTimeField(auto_now_add=True)


class FriendRequest(Model):
    sender = ForeignKey(User, on_delete=CASCADE, related_name="%(class)s_requests_sent")
    receiver = ForeignKey(User, on_delete=CASCADE, related_name="%(class)s_requests_received")


class FriendsWith(Model):
    user1 = ForeignKey(User, on_delete=CASCADE, related_name="%(class)s_requests_sent")
    user2 = ForeignKey(User, on_delete=CASCADE, related_name="%(class)s_requests_accepted")


class KeyUserForm(ModelForm):
    class Meta:
        model = KeyUser
        fields = ["username","password1","password2"]

