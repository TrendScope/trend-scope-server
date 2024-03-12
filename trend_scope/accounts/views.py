from accounts.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from static.utils.custom_exception import CheckIdExeption


@api_view(['POST'])
def check_duplicate_id(request):
    if request.method == 'POST':
        username = request.data['username']
        exist_user = User.objects.filter(username=username)

        if exist_user:
            raise CheckIdExeption()
        else:
            return Response({'detail': "회원가입이 가능한 아이디입니다."}, status=status.HTTP_200_OK)