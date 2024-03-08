from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from issues.models import Category, IssueResult, SearchWord, SearchWordCategory
from issues.serializers import CategorySerializer, AllHistorySerializer

from static.config.pagination import get_pagination_result


@api_view(['GET'])
def get_categories(request):
    if request.method == 'GET':
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(data=serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_histories(request):
    user = request.user
    if request.method == 'GET':
        sort_type = request.GET.get('type', None)
        page_size = 5
        paginator = PageNumberPagination()

        if request.GET.get("page_size"):
            paginator.page_size = page_size

        search_words = SearchWord.objects.filter(user=user)
        if search_words.exists():
            if sort_type == 'avg':
                issue_results = IssueResult.objects.filter(search_word__in=search_words).order_by('-avg_increase_rate')
            elif sort_type == 'influence':
                issue_results = IssueResult.objects.filter(search_word__in=search_words).order_by('-increase_factor')
            else:
                issue_results = IssueResult.objects.filter(search_word__in=search_words).order_by('-created_at')

            context = paginator.paginate_queryset(issue_results, request)
            paging = get_pagination_result(paginator, issue_results.count())
            serializer = AllHistorySerializer(context, many=True)
            res = {
                'page': paging,
                'data': serializer.data
            }

            return JsonResponse(res, safe=False)
        else:
            return Response({"warning":"검색 내역이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
