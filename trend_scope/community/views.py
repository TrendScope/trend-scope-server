from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from issues.models import SearchWord, IssueResult
from community.models import Post
from rest_framework.response import Response

from community.serializers import PostCreateSerializer

from static.utils.custom_exception import CheckUserSearchWordExeption


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list_create(request, search_id):
    user = request.user
    search_word = get_object_or_404(SearchWord, pk=search_id)
    issue_result = get_object_or_404(IssueResult, pk=search_word.issue_result.id)

    if request.method == 'POST':
        if SearchWord.objects.get(pk=search_id).user != user:
            raise CheckUserSearchWordExeption()
        post = Post(
            user_id=user.id,
            issue_result_id=issue_result.id,
            title=request.data["title"],
            content=request.data["content"]
        )
        post.save()
        serializer = PostCreateSerializer(instance=post, data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)