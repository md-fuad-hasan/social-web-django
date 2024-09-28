from django.urls import path 
from post import views


app_name = 'post'

urlpatterns = [
    path('upload/', views.upload, name='upload' ),
    path('like/<pk>/', views.like , name = 'like'),
    path('unlike/<pk>/', views.unlike , name = 'unlike'),

]