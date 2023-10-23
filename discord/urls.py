from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home_name"),
    path('register/', views.registerUser, name="register_url"),
    path('login/', views.loginPage, name="login_name"),
    path('logout/', views.logoutUser, name="logout_url"),
    path('roommes/<str:pk>/', views.room, name="room_name"),
    path('form/', views.create_room, name="form"),
    path('update/<str:pk>/', views.update, name="update"),
    path('delete/<str:pk>/', views.deleteRoom, name="deleteroom"),      # we access the in the <a href"{%url%}" inhtml by url name of the url
    path('delete_message/<str:pk>/', views.deletemessage, name="delete_message"),
    path('profile/<str:pk>/', views.userProfile, name="profile_page"),

]


