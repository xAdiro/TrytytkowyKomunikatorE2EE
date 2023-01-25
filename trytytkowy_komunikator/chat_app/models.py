from django.db.models import Model, CharField, DateField, DateTimeField, TextField, ForeignKey, CASCADE


class Account(Model):
    name = CharField(max_length=32)


class Key(Model):
    content = CharField(max_length=100)
    last_used = DateField(auto_now_add=True)


class Message(Model):
    author = ForeignKey(Account, on_delete=CASCADE)
    receiver_key = ForeignKey(Key, on_delete=CASCADE)
    content = TextField()
    timestamp = DateTimeField(auto_now_add=True)
