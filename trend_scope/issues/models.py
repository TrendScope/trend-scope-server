from django.db import models

from accounts.models import User

class SearchWord(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_word = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, default='ACTIVE')

class SearchWordCategory(models.Model):
    id = models.AutoField(primary_key=True)
    search_word = models.ForeignKey(SearchWord, on_delete=models.CASCADE, related_name='search_word_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class IssueResult(models.Model):
    id = models.AutoField(primary_key=True)
    search_word = models.OneToOneField(SearchWord, on_delete=models.CASCADE, related_name='issue_result')
    issue_subject = models.CharField(max_length=100)
    avg_increase_rate = models.IntegerField(default=0)
    increase_factor = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class IssueKeyword(models.Model):
    id = models.AutoField(primary_key=True)
    search_word = models.ForeignKey(SearchWord, on_delete=models.CASCADE, related_name='issue_keywords')
    issue_keyword = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)