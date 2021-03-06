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
    path('hardspotvisiterslist', views.HardspotVisitorsDownloadView.as_view(), name= "HardspotContributorDownloadView"),
    path('contentvisiterslist', views.ContentVisitorsDownloadView.as_view(), name= "ContentContributorDownloadView"),
    path('approvedhardspotdownload', views.ApprovedHardSpotDownloadView.as_view(), name= "ApprovedHardSpotDownloadView"),
    path('hardspotstatusdownload', views.HardSpotStatusDownloadView.as_view(), name= "HardSpotStatusDownloadView"),
    path('hardspotcontributorslist', views.HardspotContributorsDownloadView.as_view(), name= "HardspotContributorsDownloadView"),
    ]