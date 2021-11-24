from django.contrib import admin

from .models import *

admin.site.register(PersonalDataModel)
admin.site.register(AddressModel)
admin.site.register(SupportModel)
admin.site.register(SMSTokenModel)
admin.site.register(BookingModel)
admin.site.register(OptionsModel)
admin.site.register(CoordinatesModel)
admin.site.register(TemporaryAddressModel)
admin.site.register(TemporaryBookingModel)

#модель дополнительных параметров в админку
admin.site.register(ExtraModel)
admin.site.register(ExtraForBooking)

#модель городов
admin.site.register(CityModel)