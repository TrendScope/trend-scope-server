from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from issues.models import Category, IssueResult, SearchWord, SearchWordCategory, IssueKeyword
from issues.serializers import CategorySerializer, AllHistorySerializer, IssueKeywordSerializer, IssueResultSerializer, EmergingIssueResultSerializer
from issues.create_issues import create_issues

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

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def generate_issues(request):
    global search_word_result
    user = request.user
    if request.method == 'POST':
        search_word = request.data.get('search_word', [])
        categories = request.data.get('categories', [])
        filtered_categories = Category.objects.filter(id__in=categories)
        keywords, theme = create_issues(search_word, filtered_categories)

        # 검색어 저장
        search_word_result = SearchWord(
            user=user,
            search_word=search_word
        )
        search_word_result.save()

        # 검색어-카테고리 저장
        for category in filtered_categories:
            print(category.categoryName)
            search_word_category = SearchWordCategory(
                search_word=search_word_result,
                category=category
            )
            search_word_category.save()

        # 생성된 키워드 저장
        for keyword in keywords:
            issue_keyword = IssueKeyword(
                search_word=search_word_result,
                issue_keyword=keyword
            )
            issue_keyword.save()

        # 생성된 결과값 저장
        issue_result = IssueResult(
            search_word=search_word_result,
            issue_subject=theme
        )
        issue_result.save()
        serializer = EmergingIssueResultSerializer(issue_result)
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)