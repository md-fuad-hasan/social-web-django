from django.urls import path
from account import views

app_name = "account"

urlpatterns = [
    path('signup/', views.signup , name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('search-user/', views.search_user, name='search_user'),
]