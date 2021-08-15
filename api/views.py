from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from django.contrib.auth.models import User

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def auth(request):
    #проверяем на то, есть ли поле с номером телефона
    phone = request.data.get('phone', None)
    if phone == 'None':
        return Response(
            data = {"message": "1"},
            status = status.HTTP_400_BAD_REQUEST
        )

    if type(phone) != str:
        return Response(
            data = {"message": "2"},
            status = status.HTTP_400_BAD_REQUEST
        )

    #проверка то, цифры ли это
    int_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in range(0, len(phone)):
        if phone[i] not in int_arr:
            return Response(
                data = {"message": "3"},
                status = status.HTTP_400_BAD_REQUEST
            )

    #проверка на то, что сделдать, создать аккаунт или поработаь с прежним
    
    

    return Response(content)
