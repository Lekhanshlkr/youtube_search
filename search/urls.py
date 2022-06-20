from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('table/',views.VideoList.as_view()),
]