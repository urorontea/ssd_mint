from django.urls import path
from . import views

urlpatterns = [
    path('',views.get_name, name="get_name"),
    path('download/', views.download, name="download"),
    path("getname/", views.get_name, name="get_name"),
    #path("input_urls/", views.input_urls, name="input_urls"),
    path("input_urls_1/", views.input_urls_1, name="input_urls_1"),
    path("input_urls_2/", views.input_urls_2, name="input_urls_2"),
    path("input_urls_3/", views.input_urls_3, name="input_urls_3"),
]