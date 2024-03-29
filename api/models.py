from django.db import models
from django.contrib.auth.models import User


class CityModel(models.Model):
    """модель для городов"""
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=200, unique=True)
    coefficient = models.FloatField()
    mail = models.EmailField()


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

    # для подтверждения аккаунта
    code = models.CharField(max_length=6)

    # фото аккаунта
    photo = models.ImageField(upload_to='user_photo/', null=True, blank=True)


class ExtraModel(models.Model):
    """модель для дополнительных услуг"""

    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=100)
    multiple = models.BooleanField()
    price = models.IntegerField()

    # при каких типах уборки есть эта услуга
    type_regular = models.BooleanField()
    type_general = models.BooleanField()
    type_after_repair = models.BooleanField()

    # при каких типах помещения есть эта услуга
    type_building_flat_regular = models.BooleanField()
    type_building_office = models.BooleanField()
    type_building_house = models.BooleanField()
    type_building_cafe = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "дополнительно"
        verbose_name_plural = "дополнительная услуга"


class CoordinatesModel(models.Model):
    """эта модель нужна для координат"""

    id = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    latitudeDelta = models.FloatField()
    longitudeDelta = models.FloatField()


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

    # для координат
    coordinates = models.ForeignKey(CoordinatesModel, on_delete=models.SET_NULL, null=True)


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
    paid = models.IntegerField()

    # для выбора для почты
    city = models.CharField(max_length=200)


class ExtraForBooking(models.Model):
    """модель для заказа и параметров, которые использоватесь в моделе"""

    id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(BookingModel, on_delete=models.CASCADE)
    extra = models.ForeignKey(ExtraModel, on_delete=models.CASCADE)    
    quantity = models.IntegerField()


# модели для временных данных
class TemporaryAddressModel(models.Model):
    """эта модель создана для временного адреса"""

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

    # для координат
    coordinates = models.ForeignKey(CoordinatesModel, on_delete=models.SET_NULL, null=True)


class TemporaryBookingModel(models.Model):
    """эта модель создана для временной оплаты"""

    id = models.AutoField(primary_key=True)
    adress = models.OneToOneField(TemporaryAddressModel, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    payment_tupe = models.CharField(max_length=100)
    bonus_size = models.IntegerField()
    company_status = models.CharField(max_length=100)
    paid = models.IntegerField()

    # для выбора для почты
    city = models.CharField(max_length=200)


class TemporaryExtraForBooking(models.Model):
    """модель для дополнительных услуг(временно)"""

    id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(TemporaryBookingModel, on_delete=models.CASCADE)
    extra = models.ForeignKey(ExtraModel, on_delete=models.CASCADE) 
    quantity = models.IntegerField()


class TemporaryIdPayModel(models.Model):
    """эта модель нужна для создания платежа"""

    id = models.AutoField(primary_key=True)
    booking = models.OneToOneField(TemporaryBookingModel, on_delete=models.CASCADE)
    id_pay = models.TextField()


# служебная модель
class OptionsModel(models.Model):
    """модель параметров для калькулятора"""

    id = models.AutoField(primary_key=True)

    # типы уборки
    type_regular = models.FloatField()
    type_general = models.FloatField()
    type_after_repair = models.FloatField()

    # типы помещения
    type_building_flat = models.FloatField()
    type_building_office = models.FloatField()
    type_building_house = models.FloatField()
    type_building_cafe = models.FloatField()

    # остальные параметры
    area = models.FloatField()
    door = models.FloatField()
    window = models.FloatField()
    bathroom = models.FloatField()

    mkad = models.FloatField()
