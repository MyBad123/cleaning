import os
import random
import requests
import yookassa

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

#для почты
import smtplib

from email.mime.multipart import MIMEMultipart      
from email.mime.text import MIMEText                
from email.mime.image import MIMEImage

#мои файлы
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
            data = {
                "main_info": data,
                "phone": request.user.username
            }
        )        
    except:
        return Response(
            data = {"message": "8"},
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
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
            data = {"message": "11"},
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
    if serializer.is_valid(raise_exception=False):
        serializer.save()
    else:
        return Response(
            data = {"message": "12"},
            status = status.HTTP_400_BAD_REQUEST
        )

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
            data = {"message": "13"},
            status = status.HTTP_400_BAD_REQUEST
        )

    #проверка данных 
    serializer = UpdateSerializer(
        instance = adress_object,
        data = request.data
    )

    if serializer.is_valid(raise_exception=False):
        serializer_save = serializer.save()
    else:
        return Response(
            data = {"message": "13.1"},
            status = status.HTTP_400_BAD_REQUEST
        )

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
            data = {"message": "14"},
            status = status.HTTP_400_BAD_REQUEST
        )

    return Response(
        data = UpdateSerializer(adress_object).data
    )

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_payment(request):
    '''это для того, чтоб создать платеж''' 
    
    #проверка на правильность написания способа оплаты
    try:
        payment_tupe = request.data.get('booking').get('payment_tupe')
        if (payment_tupe != 'cash') and (payment_tupe != 'card'):
            return Response(
                data = {"message": "1"},
                status = status.HTTP_400_BAD_REQUEST
            )
    except:
        return Response(
            data = {"message": "3"},
            status = status.HTTP_400_BAD_REQUEST
        )

    #проверка на наличие бонусов
    try:
        bonus_size = request.data.get('booking').get('bonus_size')
        bonus_balance = PersonalDataModel.objects.get(user=request.user).bonus_balance
        if int(bonus_size) > int(bonus_balance):
            return Response(
                data = {"message": "4"},
                status = status.HTTP_400_BAD_REQUEST
            )
    except:
        return Response(
            data = {"message": "5"},
            status = status.HTTP_400_BAD_REQUEST
        )
    
    #достаем цену из адреса 
    try:
        price = request.data.get('adress').get('price')
    except:
        return Response(
            data = {"message": "6"},
            status = status.HTTP_400_BAD_REQUEST
        )

    if (type(price) != int):
        return Response(
            data = {"message": "7"},
            status = status.HTTP_400_BAD_REQUEST
        )

    if (price < 0):
        return Response(
            data = {"message": "8"},
            status = status.HTTP_400_BAD_REQUEST
        )

    #удаляем из временных данных объект
    if len(TemporaryAddressModel.objects.filter(user=request.user)) > 0:
        for_delete = TemporaryAddressModel.objects.get(user=request.user)
        for_delete_coords = for_delete.coordinates
        for_delete.delete()
        for_delete_coords.delete()


    #после успешного создания платежа закидываем данные во временные данные(предварительно проверяем)
    if not BookingBookingSerializer(data=request.data.get('booking', {})).is_valid(raise_exception=False):
        return Response(
            data = {"message": "9"},
            status = status.HTTP_400_BAD_REQUEST
        )
    if not BookingAdressSerializer(data=request.data.get('adress', {})).is_valid(raise_exception=False):
        return Response(
            data = {"message": "10"},
            status = status.HTTP_400_BAD_REQUEST
        )

    
    #получить координаты
    coords_object = CoordinatesModel.objects.create(
        **request.data['adress'].pop('coordinates')
    )

    adress_object = TemporaryAddressModel.objects.create(
        user = request.user,
        coordinates = coords_object,
        **request.data.get('adress')
    )
    booking_object = TemporaryBookingModel.objects.create(
        adress = adress_object,
        company_status = 'new',
        **request.data.get('booking')
    )

    if payment_tupe == 'card':
        #создаем платеж
        yookassa.Configuration.configure('823848', 'live_NYj6S7t_FN_beWVPZTrolQ-8TdssWpO04U-xwYCuDBA')
        payment = yookassa.Payment.create({
            "amount": {
                "value": str(price) + ".00", 
                "currency": "RUB"
            }, 
            "confirmation": {
                "type": "embedded"
            },
            "capture": True,
            "description": "описание"
        })

        TemporaryIdPayModel.objects.create(
            booking = booking_object,
            id_pay = payment.id
        )

        return Response(data={
            "id": payment.id,
            "token": payment.confirmation.confirmation_token
        })    
    else:
        return Response()

def my_send_mail(booking_object):
    #формируем ссылку на карту
    a1 = booking_object.adress.coordinates.latitude
    a1 = str(a1).replace(',', '.')

    a2 = booking_object.adress.coordinates.longitude
    a2 = str(a2).replace(',', '.')
    
    

    map_ref = 'http://maps.google.com/maps?q=' + a1 + ',' + a2 + '&z=17'
    print(map_ref)

    #разбираемся с переменными
    data_for_html = {
        'value1': str(booking_object.id),
        'value3': booking_object.payment_tupe,
        'value4': booking_object.adress.cleaning_type,
        'value5': booking_object.adress.premises_type,
        'value6': str(booking_object.adress.area),
        'value7': str(booking_object.adress.door),
        'value8': str(booking_object.adress.window),
        'value9': str(booking_object.adress.bathroom),
        'value10': str(booking_object.adress.mkad),
        'value11': booking_object.adress.adress,
        'value12': str(booking_object.adress.flat_or_office),
        'value13': str(booking_object.adress.comment),
        'value14': map_ref,
        'value15': str(booking_object.date),
        'value16': str(booking_object.time),
        'value17': str(booking_object.bonus_size),
        'value18': str(booking_object.adress.price)
    }

    #создаем письмо
    addr_from = "gena.kuznetsov@internet.ru"
    addr_to   = "genag4448@gmail.com"
    password  = "o%pdUaeIUI12"

    msg = MIMEMultipart()                               
    msg['From']    = addr_from                          
    msg['To']      = addr_to                            
    msg['Subject'] = 'Заказ №' + str(booking_object.id) + ' M-Cleaning'

    html = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<style>
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box; 
        font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif 
    }}
    .wow1 {{
        margin-bottom: 10px;
        text-align: center;
    }}
    .wow {{
        margin-bottom: 10px;
        margin-top: 10px;
        text-align: center;
    }}
</style>
<body>
    <h1 class="wow1">Заказ: №{value1}</h1>
    <p>Метод оплаты: {value3}</p>
    <h1 class="wow">Состав заказа</h1>
    <p>Тип уборки: {value4}</p>
    <p>Тип помещения: {value5}</p>
    <p>Площадь помещения: {value6} м2</p>
    <p>Моем дверей: {value7} шт.</p>
    <p>Моем окон: {value8} шт.</p>
    <p>Моем санузлов: {value9} шт.</p>
    <p>Расстояние от МКАД: {value10} км.</p>
    <h1 class="wow">Местоположение</h1>
    <p>Местоположение: {value11}</p>
    <p>Квартира/Офис: {value12}</p>
    <p>Подробнее: {value13}</p>
    <p>Ссылка на карту: <a href="{value14}">ссылка</a></p>
    <h1 class="wow">Дата и время</h1>
    <p>Дата уборки: {value15}</p>
    <p>Время уборки: {value16}</p>
    <h1 class="wow">Стоимость</h1>
    <p>Бонусов потрачено: {value17}</p>
    <p>Стоимость заказа: {value18}</p>
</body>
</html>
""".format(**data_for_html)

    msg.attach(MIMEText(html, 'html', 'utf-8'))
    server = smtplib.SMTP('smtp.mail.ru: 25')
    server.starttls()
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def confirm_payment(request):
    '''этот запрос для подтверждения покупки'''

    #проверяем, есть ли вообще у пользователя временные данные
    if len(TemporaryBookingModel.objects.filter(adress__user=request.user)) == 0:
        return Response(
            data = {"message": "1"},
            status = status.HTTP_400_BAD_REQUEST
        )
    else:
        temporary_booking = TemporaryBookingModel.objects.get(adress__user=request.user)

    if temporary_booking.payment_tupe == 'card':
        #проверка, были ли данные вообще у пользователя
        try:
            pay_id = TemporaryIdPayModel.obejcts.get(booking__adress__user=request.user).id_pay
        except:
            return Response(
                data = {"message": "2"},
                status = status.HTTP_400_BAD_REQUEST
            )

        #работа с проверкой оплаты
        yookassa.Configuration.configure('823848', 'live_NYj6S7t_FN_beWVPZTrolQ-8TdssWpO04U-xwYCuDBA')
        try:
            payment = yookassa.Payment.find_one(pay_id)
        except:
            return Response(
                data = {"message": "3"},
                status = status.HTTP_400_BAD_REQUEST
            )

        #проверяем соответствие между суммами
        temporary_address = TemporaryAddressModel.objects.get(user=request.user)
        if str(payment.amount.value) != (str(temporary_address.price) + '.00'):
            return Response(
                data = {"message": "4"},
                status = status.HTTP_400_BAD_REQUEST
            )
    elif temporary_booking.payment_tupe == 'cash':
        temporary_address = TemporaryAddressModel.objects.get(user=request.user)
    else:
        return Response(
            data = {"message": "5"},
            status = status.HTTP_400_BAD_REQUEST
        )

    #заполнение основных данных 
    address_model = AddressModel.objects.create(
        user = request.user, 
        cleaning_type = temporary_address.cleaning_type,
        premises_type = temporary_address.premises_type,
        area = temporary_address.area,
        door = temporary_address.door,
        window = temporary_address.window,
        bathroom = temporary_address.bathroom,
        adress = temporary_address.adress,
        flat_or_office = temporary_address.flat_or_office,
        mkad = temporary_address.mkad,
        comment = temporary_address.comment,
        price = temporary_address.price,
        bonuce = temporary_address.bonuce,
        coordinates = temporary_address.coordinates
    )
    
        
    booking_object = BookingModel.objects.create(
        adress = address_model,
        date = temporary_booking.date,
        time = temporary_booking.time,
        payment_tupe = temporary_booking.payment_tupe,
        bonus_size = temporary_booking.bonus_size,
        company_status = temporary_booking.company_status
    )
    
    temporary_address.delete()

    #работа с балансом 
    personal_object = PersonalDataModel.objects.get(user=request.user)
    personal_object.bonus_balance = (personal_object.bonus_balance - int(booking_object.bonus_size) + address_model.bonuce)
    personal_object.save()

    #работа с смс 
    try:
        message = 'Ваш заказ № ' + str(booking_object.id) + ' на сумму ' + str(booking_object.adress.price) + ' подтвержден'
        this_url = 'https://sms.ru/sms/send?api_id=' + SMSTokenModel.objects.all()[0].token + 'to=' + request.user.username + '&msg=' + message + '&json=1'
        requests.get(this_url)
    except:
        pass

    #отправить сообщение
    my_send_mail(booking_object)

    return Response()

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def set_or_get_token(request):
    '''данный запрос используется для получения и выведения токена'''

    token = request.data.get('token', None)
    
    if ((type(token) != str) or (token == '')) and (token != None):
        return Response(
            data = {"message": "23"},
            status = status.HTTP_400_BAD_REQUEST
        )
    
    if token != None:
        for i in SMSTokenModel.objects.all():
            i.delete()
        a = SMSTokenModel.objects.create(
            token = token
        )
        return Response(data={
            "token": token
        })
    else:
        if len(SMSTokenModel.objects.all()) < 1:
            return Response(
                data = {"message": "24"},
                status = status.HTTP_400_BAD_REQUEST
            ) 
        else:
            a = SMSTokenModel.objects.all()[0].token
            return Response(data={
                "token": a
            })
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_options(request):
    '''представление для данных калькулятора'''

    if len(OptionsModel.objects.all()) > 0:
        return Response(
            data=OptionsSerializer(OptionsModel.objects.all()[0]).data
        )
    else:
        return Response(data={
            'type_regular': 1.0, 
            'type_general': 1.0, 
            'type_after_repair': 1.0, 
            'type_building_flat': 1.0, 
            'type_building_office': 1.0, 
            'type_building_house': 1.0, 
            'type_building_cafe': 1.0, 
            'area': 1.0, 
            'door': 1.0, 
            'window': 1.0, 
            'bathroom': 1.0, 
            'mkad': 1.0
        })

