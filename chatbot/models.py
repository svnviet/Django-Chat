from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ChatbotIntent(models.Model):
    name = models.CharField(max_length=500)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chat_bot_intent'


class ChatBotResponse(models.Model):
    intent = models.ForeignKey(ChatbotIntent, on_delete=models.CASCADE)
    name = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chat_bot_response'


class Sentence(models.Model):
    intent = models.ForeignKey(ChatbotIntent, on_delete=models.CASCADE)
    name = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chat_bot_sentence'
