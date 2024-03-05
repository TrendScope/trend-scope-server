from django.shortcuts import render
from rest_framework import request
from rest_framework.decorators import api_view
from rest_framework.response import Response

from issues.models import Category
from issues.serializers import CategorySerializer


@api_view(['GET'])
def get_categories(request):
    if request.method == 'GET':
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(data=serializer.data)