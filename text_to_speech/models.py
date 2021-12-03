from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import mutagen
from pydub import AudioSegment


# Create your models here.

class StoreAudio(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    due_time = models.FloatField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    audio = models.FileField(upload_to='audios/')
    text = models.CharField(max_length=500)

    class Meta:
        db_table = 'text_to_speech_store_audio'

    # length = models.FloatField(blank=True)

    # def change_speed_audio(self, speed):
    #     audio_tmp = self.audio
    #     audio_info = mutagen.File(audio_tmp).info
    #     sound = AudioSegment(
    #         # raw audio data (bytes)
    #         data=b'…',
    #         # 2 byte (16 bit) samples
    #         sample_width=2,
    #         # 44.1 kHz frame rate
    #         frame_rate=44100,
    #         # stereo
    #         channels=2
    #     )

    # self.length = audio_info
    # return

    def update_audio_duration_seconds(self):
        audio_tmp = self.audio
        audio_info = mutagen.File(audio_tmp).info
        self.due_time = audio_info.length
        # self.update(due_time=audio_info.length)

    def speed_change(self, speed=1.0):
        # Manually override the frame_rate. This tells the computer how many
        # samples to play per second
        sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * speed)
        })
        # convert the sound with altered frame rate to a standard frame rate
        # so that regular playback programs will work right. They often only
        # know how to play audio at standard frame rate (like 44.1k)
        return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

    # slow_sound = speed_change(sound, 0.75)
    # fast_sound = speed_change(sound, 2.0)
