from django.urls import path
from . import views
urlpatterns = [
    path('',views.StLogin,name="StLogin"),
    path('Submit/',views.Submition,name="Submition"),
    path('favicon.ico', views.empty_favicon_view, name="empty_favicon"),
    path('<str:InstituteCode>/',views.QuesHandler ,name="Ques"),
]