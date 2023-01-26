from django.db.models import Model, CharField, DateField, DateTimeField, TextField, ForeignKey, CASCADE
from django.contrib.auth.models import User


class Key(Model):
    content = CharField(max_length=100)
    last_used = DateField(auto_now_add=True)


class Message(Model):
    author = ForeignKey(User, on_delete=CASCADE)
    receiver_key = ForeignKey(Key, on_delete=CASCADE)
    author_content = TextField()
    receiver_content = TextField()
    timestamp = DateTimeField(auto_now_add=True)


class FriendRequest(Model):
    sender = ForeignKey(User, on_delete=CASCADE, related_name="%(class)s_requests_sent")
    receiver = ForeignKey(User, on_delete=CASCADE, related_name="%(class)s_requests_received")


class FriendsWith(Model):
    user1 = ForeignKey(User, on_delete=CASCADE, related_name="%(class)s_requests_sent")
    user2 = ForeignKey(User, on_delete=CASCADE, related_name="%(class)s_requests_accepted")
