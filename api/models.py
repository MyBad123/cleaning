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
    bonus_balance = models.IntegerField()

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
    adress = models.TextField()
    flat_or_office = models.CharField(max_length=100, null=True, blank=True)
    mkad = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    bonuce = models.IntegerField()
    

class SupportModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=100)
    text = models.TextField()
    answer = models.TextField(null=True, blank=True)

class SMSTokenModel(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.TextField()

class BookingModel(models.Model):
    id = models.AutoField(primary_key=True)
    adress = models.ForeignKey(AddressModel, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    payment_tupe = models.CharField(max_length=100)
    bonus_size = models.IntegerField()
    company_status = models.CharField(max_length=100)









