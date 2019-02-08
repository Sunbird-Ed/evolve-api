from django.urls import path, include
from apps.hardspot import views

urlpatterns = [
    path('hardspot_details', views.BookNestedList.as_view(), name = 'BookNestedList'),
    path('hardspotdetailupdate/<int:pk>', views.HardSpotUpdateView.as_view(), name= "HardSpotUpdateView"),
    path('hardspotlist', views.HardSpotListOrCreateView.as_view(), name = 'hardspotlist'),
    path('approved', views.HardSpotApprovedList.as_view(), name = 'HardSpotApprovedList'),
    path('pending', views.HardSpotPendingList.as_view(), name = 'HardSpotPendingList'),
    path('rejected', views.HardSpotRejectedList.as_view(), name = 'HardSpotRejectedList'),
    path('hardSpotstatuslist', views.HardSpotStatusList.as_view(), name= "HardSpotStatusList"),
    path('hardspotcontributors', views.HardSpotContributorCreateView.as_view(), name= "HardSpotContributorCreate"),
    path('hardspotvisiterslist', views.HardspotContributorDownloadView.as_view(), name= "HardspotContributorDownloadView"),
    path('contentvisiterslist', views.ContentContributorDownloadView.as_view(), name= "ContentContributorDownloadView"),
    path('hardspotstatusdownload', views.HardSpotStatusDownloadView.as_view(), name= "HardSpotStatusDownloadView"),
    path('contentstatusdownload', views.ContentStatusDownloadView.as_view(), name= "ContentStatusDownloadView")
  
    ]