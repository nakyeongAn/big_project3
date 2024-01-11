from django.db import models
from django.conf import settings

class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='accounts_friend_requests_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='accounts_friend_requests_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='sent')

    def __str__(self):
        return f"Friend request from {self.sender} to {self.receiver}"

class Friendship(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="friendship_user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="friendship_user2", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1.username} and {self.user2.username}"
from django.conf import settings


# 대화가 끝나서 결과 -> 확인
class Conversation(models.Model):
    # 대화 id
    id = models.AutoField(primary_key=True)
    # 주는 사람(로그인한사람)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='conversations_as_sender', on_delete=models.CASCADE)
    # 받는 사람
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='conversations_as_receiver', on_delete=models.CASCADE)
    # 채팅 시작 시간
    start_time = models.DateTimeField(auto_now_add=True)
    # 채팅 끝난 시간
    end_time = models.DateTimeField(null=True, blank=True)
    # 채팅 완료 여부
    end_status = models.BooleanField(default = False)
    # 추천된 3개의 상품
    items = models.CharField(max_length=200, blank=True, default='')

    


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    bot_content = models.CharField(max_length=2000, null=True, blank=True)  
    user_content = models.CharField(max_length=2000, null=True, blank=True)  
    timestamp = models.DateTimeField(auto_now_add=True)


class GiftRequest(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.BigIntegerField(blank=True, null=True)
    receiver = models.BigIntegerField(blank=True, null=True)
    additionalinfo = models.TextField(null=True, blank=True)
    minamount = models.BigIntegerField(null=True, blank=True)
    maxamount = models.BigIntegerField(null=True, blank=True)
    relationship = models.CharField(max_length=30, blank=True, null=True)
    occasion = models.CharField(max_length=30, blank=True, null=True)
    is_completed = models.BooleanField(default=False)
 
 # 대화가 끝나서 결과 -> 확인
class Three(models.Model):
    # 대화 id
    id = models.AutoField(primary_key=True)
    # 주는 사람(로그인한사람)
    sender = models.BigIntegerField(blank=True, null=True)
    # 받는 사람
    receiver = models.BigIntegerField(blank=True, null=True)
    # 추천된 3개의 상품
    three_products = models.CharField(max_length=200, blank=True, default='')