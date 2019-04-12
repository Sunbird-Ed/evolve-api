from django.urls import path, include
from apps.content import views

urlpatterns = [
    path('othercontributors', views.OtherContributorCreateView.as_view(), name = 'OtherContributorCreateView'),
    ]