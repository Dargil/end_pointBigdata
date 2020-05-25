from django.conf.urls import include
from rest_framework import routers
from .viewsets import *
from django.urls import path
from .views import *

router=routers.SimpleRouter()


urlpatterns = [
    path('new_evento/',new_evento),
    path('', include(router.urls)),
]