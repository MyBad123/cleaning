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

    #test
    path('test/', test),
]
