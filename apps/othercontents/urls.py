from django.urls import path, include
from apps.othercontents import views

urlpatterns = [
    path('othercontributors', views.OtherContributorCreateView.as_view(), name = 'OtherContributorCreateView'),
    path('othercontentlist', views.OtherContentList.as_view(), name = 'OtherContentList'),
    ]