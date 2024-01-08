from django.db import models
from django.conf import settings
from django.utils import timezone

class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일자 필드 추가
    views = models.PositiveIntegerField(default=0)
    is_answered = models.BooleanField(default=False)  # 관리자 답변 여부

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일자 필드 추가

    def __str__(self):
        return self.content
