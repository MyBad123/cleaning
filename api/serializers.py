from rest_framework import serializers

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

