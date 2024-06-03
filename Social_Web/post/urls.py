from django.urls import path 
from post import views


app_name = 'post'

urlpatterns = [
    path('upload/', views.upload, name='upload' )
]