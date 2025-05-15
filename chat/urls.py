# chat/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='chat_index'),
    path('signup/', views.signup_view, name='signup'),
    path('<int:chat_id>/', views.chat_detail, name='chat_detail'),

]
