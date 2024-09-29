from django.urls import path 
from post import views


app_name = 'post'

urlpatterns = [
    path('upload/', views.upload, name='upload' ),
    path('like/<pk>/', views.like , name = 'like'),
    path('unlike/<pk>/', views.unlike , name = 'unlike'),
    path('detail-post/<pk>', views.detail_post, name='detail_post'),
    path('delete-post/<pk>', views.delete_post, name='delete_post')
]