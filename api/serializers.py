from rest_framework import serializers

from .models import *

class PersonalDataSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True)
    surname = serializers.CharField(allow_null=True)
    patronymic = serializers.CharField(allow_null=True)
    company = serializers.BooleanField()
    inn = serializers.IntegerField(allow_null=True)
    mail = serializers.EmailField(allow_null=True)
    balance = serializers.IntegerField(allow_null=True)
    bonus_balance = serializers.IntegerField(allow_null=True)
    photo = serializers.ImageField(allow_null=True)

class SecondPersonalDataSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True)
    surname = serializers.CharField(allow_null=True)
    patronymic = serializers.CharField(allow_null=True)
    company = serializers.BooleanField()
    inn = serializers.IntegerField(allow_null=True)
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
    answer = serializers.CharField()
    text = serializers.CharField(allow_null=True)

    def update(self, instance, validated_data):
        return SupportModel.objects.create(
            user = instance,
            question_type = validated_data.get("question_type"),
            text = validated_data.get("text"),
            answer = None
        ) 

###def create(self, validated_data):
###        return Article.objects.create(**validated_data)

class YourAdressSerializer(serializers.ModelSerializer):
    '''сериализатор для экрана ВАШИ АДРЕСА'''

    class Meta:
        model = AddressModel
        fields = [
            'id', 'flat_or_office',
            'area', 'adress', 'flat_or_office',
            'price'
        ]

class UpdateSerializer(serializers.ModelSerializer):
    '''сериализатор для обновления адреса'''

    class Meta:
        model = AddressModel
        fields = [
            'id', 'cleaning_type',
            'premises_type', 'area', 'door',
            'window', 'bathroom', 'adress',
            'flat_or_office', 'mkad', 
            'comment', 'price',
            'bonuce'
        ]

    def update(self, instance, validated_data):
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

        instance.save()
        return instance

class BookingAdressSerializer(serializers.ModelSerializer):
    '''сериализатор для покупки'''

    class Meta:
        model = AddressModel
        fields = [
            'cleaning_type',
            'premises_type', 'area', 'door',
            'window', 'bathroom', 'adress',
            'flat_or_office', 'mkad', 
            'price', 'bonuce'
        ]

class BookingBookingSerializer(serializers.ModelSerializer):
    '''сериализатор для покупки'''

    class Meta:
        model = BookingModel
        fields = [
            'date', 'time', 
            'payment_tupe', 'bonus_size', 
        ]