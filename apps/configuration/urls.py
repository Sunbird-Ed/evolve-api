from django.urls import path, include
from apps.configuration import views

urlpatterns=[
    path('detailslist',views.DetailList.as_view(),name='booklist')

]