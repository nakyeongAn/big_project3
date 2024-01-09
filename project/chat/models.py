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
