from rest_framework.exceptions import APIException

class CheckIdExeption(APIException):
    status_code = 409
    default_detail = '회원가입할 수 없는 아이디입니다.'
    default_code = '4091'