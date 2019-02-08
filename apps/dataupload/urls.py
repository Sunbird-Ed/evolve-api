from django.urls import path, include
from apps.dataupload import views

urlpatterns=[
    path('tocupload', views.TOCUploadView.as_view(), name = 'TOCUploadView'),
]