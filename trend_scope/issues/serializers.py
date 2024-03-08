from issues.models import Category, SearchWordCategory, IssueResult, SearchWord
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'categoryName']


class IssueResultSerializer(serializers.ModelSerializer):
    issue_result_id = SerializerMethodField(method_name='get_issue_result_id')
    issue_result_subject = SerializerMethodField(method_name='get_issue_result_subject')

    class Meta:
        model = IssueResult
        fields = ['issue_result_id', 'issue_result_subject', 'avg_increase_rate', 'increase_factor']

    def get_issue_result_id(self, obj):
        return obj.id

    def get_issue_result_subject(self, obj):
        return obj.issue_subject


class SearchWordCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchWordCategory
        fields = ['category_id']

class AllHistorySerializer(serializers.ModelSerializer):
    search_word = SerializerMethodField(method_name='get_search_word')
    issue_result_id = SerializerMethodField(method_name='get_issue_result_id')
    issue_result_subject = SerializerMethodField(method_name='get_issue_result_subject')
    search_word_categories = SerializerMethodField(method_name='get_search_word_categories')

    class Meta:
        model = IssueResult
        fields = ['search_word', 'issue_result_id', 'issue_result_subject',
                  'avg_increase_rate', 'increase_factor', 'search_word_categories']

    def get_search_word(self, obj):
        return obj.search_word.search_word

    def get_issue_result_id(self, obj):
        return obj.id

    def get_issue_result_subject(self, obj):
        return obj.issue_subject

    def get_search_word_categories(self, obj):
        search_word = obj.search_word
        serializer = SearchWordCategorySerializer(search_word.search_word_categories, many=True, read_only=True)
        return serializer.data