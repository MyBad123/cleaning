from django.contrib import admin

from .models import *

admin.site.register(PersonalDataModel)
admin.site.register(AddressModel)
admin.site.register(SupportModel)
admin.site.register(SMSTokenModel)
admin.site.register(BookingModel)
admin.site.register(BalancePlusHistory)

