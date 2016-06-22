from django.conf.urls import url, include
from django.contrib import admin
from interface.views import *
urlpatterns = [
url(r'^interface/',include(interface.urls),namespace='')]