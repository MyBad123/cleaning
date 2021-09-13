import os
import random

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from .models import *
from .serializers import *

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def auth(request):
    '''авторизация аккаунта'''
    
    #проверяем на то, есть ли поле с номером телефона
    phone = request.data.get('phone', None)
    if phone == None:
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

    #проверка на то, не пустая ли строка
    if phone == '':
        return Response(
            data = {"message": "4"},
            status = status.HTTP_400_BAD_REQUEST
        )

    #проверка на то, что сделдать, создать аккаунт или поработаь с прежним
    if len(User.objects.filter(username=phone)) > 0:
        user = User.objects.filter(username=phone)[0]
        personal_data = PersonalDataModel.objects.get(user=user)
        personal_data.code = str(random.randint(100000, 999999))
        
        ###########work with phone##########

        ####################################
        return Response()
    else:
        user = User.objects.create_user(
            username = phone,
            email = None,
            password = str(random.randint(100000, 999999))
        )
        personal_data = PersonalDataModel.objects.create(
            user = user, 
            code = str(random.randint(100000, 999999)),
            balance = 0,
            bonus_balance = 0, 
            company = False
        )
        Token.objects.create(
            user = user
        )

        ###########work with phone##########

        ####################################
        return Response()
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def code(request):
    '''проверка кода'''

    #достаем телефон и код
    phone = request.data.get('phone', None)
    code = request.data.get('code', None)

    #проверяем на валидность телефон и код
    if (type(phone) != str) or (type(code) != str):
        return Response(
            data = {"message": "5"},
            status = status.HTTP_400_BAD_REQUEST
        )

    #достаем пользователя
    user = None
    try:
        user = User.objects.get(username=phone)
    except:
        return Response(
            data = {"message": "6"},
            status = status.HTTP_400_BAD_REQUEST
        )   

    #сверяемся с полученным пользователем и его кодом
    try:
        PersonalDataModel.objects.get(user=user, code=code)
        return Response(data={
            "token": Token.objects.get(user=user).key
        })
    except:
        return Response(
            data = {"message": "7"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def account(request):
    '''получить персональные данные аккаунта'''

    data = None 
    try:
        #достаем данные пользователя и серриализуем их
        personal_data = PersonalDataModel.objects.get(user=request.user)
        data = PersonalDataSerializer(personal_data).data

        return Response(
            data = data,
            status = status.HTTP_400_BAD_REQUEST
        )        
    except:
        return Response(
            data = {"message": "8"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_account(request):
    '''обновить персональные данные аккаунта'''

    #достаем пользователя
    personal_data = None
    try:
        personal_data = PersonalDataModel.objects.get(
            user = request.user
        )
    except:
        return Response(
            data = {"message": "9"},
            status = status.HTTP_400_BAD_REQUEST
        )
    
    data = None

    #серриализуем данные
    serializer = SecondPersonalDataSerializer(instance=personal_data, data=request.data)
    if serializer.is_valid(raise_exception=False):
        try:
            os.remove(personal_data.photo.path)
        except:
            pass

        data = serializer.save()
    else:
        return Response(
            data = {"message": "10"},
            status = status.HTTP_400_BAD_REQUEST
        )

    return Response(
        data = PersonalDataSerializer(data).data
    )

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_questions(request):
    '''вывести все вопросы'''

    #вывести список всех вопросов тех.поддержке 
    support = None
    try:
        support = SupportModel.objects.filter(user=request.user)
    except:
        return Response(
            data = {"message": "10"},
            status = status.HTTP_400_BAD_REQUEST
        )
    
    return Response(data=SupportSerializer(support, many=True).data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_questions(request):
    '''создать новый вопрос'''

    #вывести юзера 
    user = request.user
    
    #создать новый вопрос 
    serializer = SupportSerializer(instance=user, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()

    #выводим все вопросы
    support = SupportModel.objects.filter(user=user)
    return Response(data=SupportSerializer(support, many=True).data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_adress(request):
    '''получить все адреса'''

    #вывести юзера 
    user = request.user
    
    #отправить серриализованные данные 
    all_adress = AddressModel.objects.filter(user=user)
    return Response(
        data = YourAdressSerializer(all_adress, many=True).data
    )

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_adress(request):
    '''обновить како-то адрес'''

    try:
        adress_object = AddressModel.objects.get(
            id = request.data.get('id', None),
            user = request.user
        )
    except:
        return Response(
            data = {"message": "10"},
            status = status.HTTP_400_BAD_REQUEST
        )

    #проверка данных 
    serializer = UpdateSerializer(
        instance = adress_object,
        data = request.data
    )

    if serializer.is_valid(raise_exception=False):
        serializer_save = serializer.save()

    return Response(
        data = UpdateSerializer(serializer_save).data
    )

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_adress(request):
    '''получить подробно один какой-то адрес'''

    try:
        adress_object = AddressModel.objects.get(
            id = request.data.get('id', None),
            user = request.user
        )
    except:
        return Response(
            data = {"message": "10"},
            status = status.HTTP_400_BAD_REQUEST
        )

    return Response(
        data = UpdateSerializer(adress_object).data
    )

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_adress_booking(request):
    '''создать адрес(или взять готовый) и заплатить'''

    #проверка на то, верные ли данные
    if not BookingBookingSerializer(data=request.data.get('booking', {})).is_valid(raise_exception=False):
        return Response(
            data = {"message": "10"},
            status = status.HTTP_400_BAD_REQUEST
        )
    if not BookingAdressSerializer(data=request.data.get('adress', {})).is_valid(raise_exception=False):
        return Response(
            data = {"message": "10"},
            status = status.HTTP_400_BAD_REQUEST
        )

    #проверка на то, если данный адрес в таблице
    if len(AddressModel.objects.filter(user=request.user, **request.data.get('adress'))) > 0:
        adress_object = AddressModel.objects.filter(user=request.user, **request.data.get('adress'))[0]
        booking_objects = BookingModel.obejcts.create(
            adress = adress_object,
            **request.data.get('booking')
        )
        booking_objects.save()
    else:
        adress_object = AddressModel.objects.create(
            user = request.user,
            **request.data.get('adress')
        )
        BookingModel.objects.create(
            adress = adress_object,
            **request.data.get('booking')
        )

    return Response()
    

@api_view(['POST'])
@permission_classes([AllowAny])
def test(request):
    class Ser(serializers.Serializer):
        a = serializers.IntegerField()

    if Ser(data=request.data).is_valid(raise_exception=True):
        return Response()


