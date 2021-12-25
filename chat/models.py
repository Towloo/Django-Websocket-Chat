from chat.managers import ThreadManager
from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Thread(BaseModel):
    users = models.ManyToManyField('auth.User')

    objects = ThreadManager()

    def __str__(self) -> str:
        if self.users.count() == 2:
            return f'{self.users.first()} and {self.users.last()}'
        return f'{self.name}'

class Message(BaseModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    text = models.TextField(blank=False, null=False)
    read_at = models.DateTimeField(auto_now=False, null=True)

    def __str__(self) -> str:
        return f'From <Thread - {self.thread}>'