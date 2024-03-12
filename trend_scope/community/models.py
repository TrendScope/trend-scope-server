from django.db import models

from accounts.models import User

from issues.models import IssueResult


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    issue_result = models.ForeignKey(IssueResult, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_user = models.ManyToManyField(User, blank=True, related_name='liked_user')
    like_num = models.PositiveIntegerField(default=0)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
