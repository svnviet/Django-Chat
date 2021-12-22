from djongo import models
from django.contrib.auth.models import User
from datetime import datetime
import mutagen
from pydub import AudioSegment
from pymongo import MongoClient
from django.utils import timezone
from django.conf import settings
import pytz

try:
    conn = MongoClient()  # Making coonection
    db = conn.database
except:
    print("Could not connect to MongoDB")


# Create your models here.

class StoreAudio(models.Model):
    _id = models.ObjectIdField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    due_time = models.DecimalField(max_digits=100, decimal_places=2, null=True)
    due_time_display = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    created_time_zone = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    audio = models.FileField(upload_to='audios/')
    text = models.CharField(max_length=500)
    objects = models.DjongoManager()

    class Meta:
        db_table = 'text_to_speech_store_audio'
