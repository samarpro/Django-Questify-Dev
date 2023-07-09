from django.urls import path
from django.contrib.auth import views as authview
from . import views
urlpatterns =[
    path('',authview.LoginView.as_view(),name='login'),
    path('login/',authview.LoginView.as_view()),
    path('logout/',authview.LogoutView.as_view(),name='logout'),
    path('signup/',views.SignUp,name='signup')

]