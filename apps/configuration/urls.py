from django.urls import path, include
from apps.configuration import views

urlpatterns=[
    path('state', views.StateList.as_view()),
    path('medium', views.MediumList.as_view()),
    path('grade', views.GradeList.as_view()),
    path('subject', views.SubjectList.as_view()),
    path('book', views.BookList.as_view()),
    path('detailslist',views.DetailList.as_view(),name='booklist')

]