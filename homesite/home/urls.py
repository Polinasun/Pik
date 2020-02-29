from django.urls import path
from .views import *
urlpatterns = [
    path('homes/', Homes),
    path('home/<uuid:h_uuid>', Home)
]