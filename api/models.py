from django.db import models
from django.contrib.auth.models import User


class PersonalDataModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    company = models.BooleanField()
    inn = models.IntegerField(null=True, blank=True)
    mail = models.EmailField(null=True, blank=True)
    balance = models.IntegerField(null=True, blank=True)
    bonus_balance = models.IntegerField(null=True, blank=True)

    #для подтверждения аккаунта
    code = models.CharField(max_length=6)

    #фото аккаунта
    photo = models.ImageField(upload_to='user_photo/', null=True, blank=True)

class AddressModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cleaning_type = models.CharField(max_length=100)
    premises_type = models.CharField(max_length=100)
    area = models.IntegerField()
    door = models.IntegerField()
    window = models.IntegerField()
    bathroom = models.IntegerField()
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.IntegerField()
    flat_or_office = models.CharField(max_length=100)
    mkad = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    time = models.TimeField()
    price = models.IntegerField()
    bonuce = models.IntegerField()
    payment_tupe = models.CharField(max_length=100)

class SupportModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=100)
    text = models.TextField()
    answer = models.TextField(null=True, blank=True)

class MyAdress(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.IntegerField()
    flat = models.IntegerField(null=True, blank=True)
    



