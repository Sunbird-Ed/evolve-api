from django.urls import path, include
from apps.othercontents import views

urlpatterns = [
    path('othercontributors', views.OtherContributorCreateView.as_view(), name = 'OtherContributorCreateView'),
    path('othercontentlist', views.OtherContentList.as_view(), name = 'OtherContentList'),
    path('booknestedlist',views.BookNestedList.as_view(),name="BookNestedList"),
    path('schoolslist',views.SchoolNameList.as_view(),name="SchoolsList"),



    # <--------------other content review------------------->

    path('otherbooklist',views.OtherBookListView.as_view(),name="OtherBookListView"),
    path('otherapprovedlist',views.OtherContentApprovedList.as_view(),name="OtherContentApprovedListView"),
    path('otherpendinglist',views.OtherContentPendingList.as_view(),name="OtherContentPendingListView"),
    path('otherrejectedlist',views.OtherContentRejectedList.as_view(),name="OtherContentRejectedListView"),
    path('othercontentupdate/<int:pk>',views.UpdateOtherContentView.as_view(),name="UpdateOtherContentView"),
    path('othercontentdetaillist',views.OtherContentDetailList.as_view(),name="OtherContentDetailListView"),
    path('othercontributorsdownload',views.OtherContentContributorsDownloadView.as_view(),name="OtherContentContributorsDownloadView"),
    path('approvedothercontentdownload',views.ApprovedOtherContentDownload.as_view(),name="ApprovedOtherContentDownloadView"),
    path("othercontentstatusdownload",views.OtherContentStatusDownloadView.as_view(),name="OtherContentStatusDownloadView"),
    path("ApprovedOtherContentDownloadSecond",views.ApprovedOtherContentDownloadSecond.as_view(),name="ApprovedOtherContentDownloadSecondView"),
    path("filestatus",views.JobStatus.as_view(),name="JobStatusView"),  
    path("urlupdate",views.OtherContentListUrlUpdate.as_view(),name="OtherContentListUrlUpdateView"),

    path("urlputrequest",views.OtherContentListUrlPutRequest.as_view(),name='OtherContentListUrlPutRequestView'),
    path("urlputrequestrevert",views.OtherContentListUrlPutRequestRevert.as_view(),name= "OtherContentListUrlPutRequestRevertView"),
    path("backup",views.BackupOtherContent.as_view(),name ="BackupOtherContentView")


    ]