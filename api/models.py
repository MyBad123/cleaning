from django.db import models
from django.contrib.auth.models import User


class PersonalDataModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100)
    inn = models.IntegerField()
    mail = models.EmailField()
    mail = models.EmailField()
    balance = models.IntegerField()
    bonus_balance = models.IntegerField()

class AddressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cleaning_type = models.CharField(max_length=100)
    premises_type = models.CharField(max_length=100)
    area = models.IntegerField()
    door = models.IntegerField()
    window = models.IntegerField()
    bathroom = models.IntegerField()
    



