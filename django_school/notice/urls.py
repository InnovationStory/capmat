from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    #Notification list
    path('list/', views.CommentNoticeListView.as_view(), name='list'),
    path('Inbox/', views.CommentNoticeListView_read.as_view(), name='inbox'),

    #Update notification status
    path('update/', views.CommentNoticeUpdateView.as_view(), name='update'),
    path('update/<int:notice_id>', views.CommentNoticeUpdateView.as_view(), name='update_article'),
       #Update notification status
    path('list/notification', views.ExpertNoticeUpdateView.as_view(), name='notification_expert'),
   
]