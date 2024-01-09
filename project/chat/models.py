from django.db import models
from django.conf import settings


# 대화가 끝나서 결과 -> 확인
class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='conversations_as_sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='conversations_as_receiver', on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    end_status = models.BooleanField(default = False)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    bot_content = models.CharField(max_length=2000, null=True, blank=True)  
    user_content = models.CharField(max_length=2000, null=True, blank=True)  
    timestamp = models.DateTimeField(auto_now_add=True)
