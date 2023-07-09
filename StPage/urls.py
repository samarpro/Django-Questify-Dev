from django.urls import path
from . import views
urlpatterns = [
    path('',views.StLogin,name="StLogin"),
    path('<str:InstituteCode>',views.QuesHandler ,name="Ques")
]