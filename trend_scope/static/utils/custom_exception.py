from rest_framework.exceptions import APIException

class CheckIdExeption(APIException):
    status_code = 409
    default_detail = '회원가입할 수 없는 아이디입니다.'
    default_code = '4091'

class CheckUserSearchWordExeption(APIException):
    status_code = 400
    default_detail = '사용자 검색 내역에 해당되지 않는 식별자입니다.'
    default_code = '4001'