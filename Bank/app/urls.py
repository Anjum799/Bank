from django.urls import path
from . import views 

urlpatterns=[
    path('',views.home,name='home'),
    path("1",views.create ,name='create'),
    path("2",views.Pin_generation, name='pin_generation'),
    path("3",views.Balance,name='balance'),
    path("4",views.deposit,name='deposit'),
    path("5",views.withdrawl,name='withdrawl'),
    path("6",views.account_transfer,name='account_transfer')
]