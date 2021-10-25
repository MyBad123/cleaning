from django.urls import path

from .views import *

urlpatterns = [
    path('auth/', auth),
    path('code/', code),
    path('account/', account),
    path('update-account/', update_account),

    #работа с тех.поддержкой
    path('get-questions/', get_questions),
    path('create-questions/', create_questions),

    #работа с адресами
    path('get-all-adress/', get_all_adress),
    path('get-adress/', get_adress),
    path('update-adress/', update_adress),
    

    #работа с токеном
    path('set-or-get-token/', set_or_get_token),


    #работа с заказами 
    #
    path('create-payment/', create_payment),
    #
    path('confirm-payment/', confirm_payment),

    #передать переменные калькулятора 
    path('get-options/', get_options),
]
