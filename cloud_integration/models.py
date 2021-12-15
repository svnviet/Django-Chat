from django.contrib.auth.models import User
from djongo import models
from chatbot.data.example import create_intent_yaml


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    objects = models.DjongoManager()

    def __str__(self):
        return self.full_name

    def create(self, *args, **kwargs):
        user = super(Customer, self).create(*args, **kwargs)
        create_intent_yaml(user)
        return user
