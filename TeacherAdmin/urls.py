from django.urls import path
from . import views
urlpatterns = [
    path('',views.dashboard,name='dash'),
    path('dashboard/',views.dashboard),
    path('upload/',views.uploadInfo,name="upload"),
    path("result",views.show_result,name ="result"),
    path("delete-row/<str:id_of_row>/",views.delete_row),
    path('edit/<int:id_object>',views.edit_object_info)
]