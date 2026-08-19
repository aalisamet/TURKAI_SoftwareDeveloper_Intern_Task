from django.urls import path
from notice_app import views

urlpatterns = [
    path('',views.red_notices, name='red_notices'),
]
