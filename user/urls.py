from django.urls import path, include
from . import views

urlpatterns=[
    path('login',views.UserDetail.as_view(),name='login')

]