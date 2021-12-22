from django.db import models
from django.contrib.auth.models import User
from djongo import models


# Create your models here.
class ChatbotIntent(models.Model):
    name = models.CharField(max_length=500)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.TextField()
    objects = models.DjongoManager()

    def __str__(self):
        return self.response

    class Meta:
        db_table = 'chat_bot_intent'


class Sentence(models.Model):
    intent = models.ForeignKey(ChatbotIntent, on_delete=models.CASCADE)
    name = models.TextField()
    objects = models.DjongoManager()

    def __str__(self):
        return self.name if self.name else ' '

    class Meta:
        db_table = 'chat_bot_sentence'
