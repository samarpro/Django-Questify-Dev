from django.urls import path
from . import views
urlpatterns = [
    path('',views.dashboard,name='dash'),
    path('dashboard/',views.dashboard),
    path('upload/',views.uploadInfo,name="upload")
]