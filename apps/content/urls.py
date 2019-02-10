from django.urls import path, include
from apps.content import views

urlpatterns = [
    path('contentlist', views.ContentList.as_view(), name = 'ContentList'),
    path('contentupdate/<int:pk>', views.ContentRetrieveUpdate.as_view(), name= 'ContentRetrieveUpdate'),
    path('booknestedlist',views.BookNestedList.as_view(),name="BookNestedList"),
    path('bookList',views.BookListView.as_view(),name="BookListView"),

    path('approved',views.ContentApprovedList.as_view(),name="ContentApprovedList"),
    path('pending',views.ContentPendingList.as_view(),name="ContentPendingList"),
    path('status',views.ContentStatusList.as_view(),name="ContentStatusList"),
    path('rejected',views.ContentRejectedList.as_view(),name="ContentRejectedList"),
    path('keywords',views.Keywords.as_view(),name="keywords"),
    path('contentcontributors', views.ContentContributorCreateView.as_view(), name= "ContentContributorCreate"),
    path('approvedcontentdownload', views.ApprovedContentDownloadView.as_view(), name= "ApprovedContentDownload"),
    path('contentstatusdownload', views.ContentStatusDownloadView.as_view(), name= "ContentStatusDownloadView"),


    ]