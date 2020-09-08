from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('load_select_buttons', views.loadSelectButtons),
    path('get_durations', views.getDurations)
]
