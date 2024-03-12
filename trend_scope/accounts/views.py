from accounts.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response


@api_view(['POST'])
def check_duplicate_id(request):
    if request.method == 'POST':
        username = request.data['username']
        exist_user = User.objects.filter(username=username)

        if exist_user:
            raise APIException(detail="이미 존재하는 아이디입니다.")
        else:
            return Response({'detail': "회원가입이 가능한 아이디입니다."}, status=status.HTTP_200_OK)