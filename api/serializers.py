from rest_framework import serializers

from .models import *

class PersonalDataSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True)
    surname = serializers.CharField(allow_null=True)
    patronymic = serializers.CharField(allow_null=True)
    company = serializers.BooleanField()
    inn = serializers.CharField(allow_null=True)
    mail = serializers.EmailField(allow_null=True)
    bonus_balance = serializers.IntegerField(allow_null=True)
    photo = serializers.ImageField(allow_null=True)

class SecondPersonalDataSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True)
    surname = serializers.CharField(allow_null=True)
    patronymic = serializers.CharField(allow_null=True)
    company = serializers.BooleanField()
    inn = serializers.CharField(allow_null=True)
    mail = serializers.EmailField(allow_null=True)
    photo = serializers.ImageField(allow_null=True)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.patronymic = validated_data.get('patronymic', instance.patronymic)
        instance.company = validated_data.get('company', instance.company)
        instance.inn = validated_data.get('inn', instance.inn)
        instance.mail = validated_data.get('mail', instance.mail)
        instance.photo = validated_data.get('photo', instance.photo)

        instance.save()
        return instance

class SupportSerializer(serializers.Serializer):
    question_type = serializers.CharField()
    text = serializers.CharField()
    answer = serializers.CharField(allow_null=True)

    def update(self, instance, validated_data):
        return SupportModel.objects.create(
            user = instance,
            question_type = validated_data.get("question_type"),
            text = validated_data.get("text"),
            answer = None
        ) 

###def create(self, validated_data):
###        return Article.objects.create(**validated_data)

class CoordinatesSerializer(serializers.ModelSerializer):
    '''серриализатор для координат'''

    class Meta:
        model = CoordinatesModel
        fields = '__all__'

class YourAdressSerializer(serializers.ModelSerializer):
    '''сериализатор для данных адреса'''

    coordinates = CoordinatesSerializer()

    class Meta:
        model = AddressModel
        fields = [
            'id', 'flat_or_office',
            'area', 'adress', 'flat_or_office',
            'price', 'premises_type','coordinates'
        ]

class YourBookingSerializer(serializers.ModelSerializer):
    '''серриализатор для страницы ВАШИ АДРЕСА'''

    adress = YourAdressSerializer()

    class Meta:
        model = BookingModel
        fields = [
            'id', 'adress'
        ]

class UpdateSerializer(serializers.ModelSerializer):
    '''сериализатор для обновления адреса'''

    coordinates = CoordinatesSerializer()

    class Meta:
        model = AddressModel
        fields = [
            'id', 'cleaning_type',
            'premises_type', 'area', 'door',
            'window', 'bathroom', 'adress',
            'flat_or_office', 'mkad', 
            'comment', 'price',
            'bonuce', 'coordinates'
        ]

    def update(self, instance, validated_data):
        #удаляем старые координаты
        old_coords = instance.coordinates
        try:
            old_coords.delete()
        except:
            pass

        #вставляем новые координаты
        data_new_coords = validated_data.pop('coordinates')
        try:
            new_coords = CoordinatesModel.objects.create(**data_new_coords)
        except:
            pass

        instance.cleaning_type = validated_data.get('cleaning_type', instance.cleaning_type)
        instance.premises_type = validated_data.get('premises_type', instance.premises_type)
        instance.area = validated_data.get('area', instance.area)
        instance.door = validated_data.get('door', instance.door)
        instance.window = validated_data.get('window', instance.window)
        instance.bathroom = validated_data.get('bathroom', instance.bathroom)
        instance.adress = validated_data.get('adress', instance.adress)
        instance.flat_or_office = validated_data.get('flat_or_office', instance.flat_or_office)
        instance.mkad = validated_data.get('mkad', instance.mkad)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.price = validated_data.get('price', instance.price)
        instance.bonuce = validated_data.get('bonuce', instance.bonuce)
        instance.coordinates = new_coords

        instance.save()
        return instance

class BookingAdressSerializer(serializers.ModelSerializer):
    '''сериализатор для покупки'''

    coordinates = CoordinatesSerializer()

    class Meta:
        model = TemporaryAddressModel
        fields = [
            'cleaning_type',
            'premises_type', 'area', 'door',
            'window', 'bathroom', 'adress',
            'flat_or_office', 'mkad', 
            'price', 'bonuce', 'coordinates'
        ]

class BookingBookingSerializer(serializers.ModelSerializer):
    '''сериализатор для покупки'''

    class Meta:
        model = TemporaryBookingModel
        fields = [
            'date', 'time', 
            'payment_tupe', 'bonus_size', 
            'paid', 'city'
        ]


class OptionsSerializer(serializers.ModelSerializer):
    '''сериализатор для данных калькулятора'''

    class Meta:
        model = OptionsModel
        exclude = ['id']

class  ExtraSerializer(serializers.ModelSerializer):
    '''сериализатор для данных о дополнительных опциях'''

    class Meta:
        model = ExtraModel
        fields = [
            'id',  'name', 'multiple', 'price'
        ]

class CitySerializer(serializers.ModelSerializer):
    '''сериализатор городов'''

    class Meta:
        model = CityModel
        fields = [
            'city', 'coefficient', 'mail'
        ]

