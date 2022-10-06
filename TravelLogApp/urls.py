from django.urls import path
from TravelLogApp.views import *
from TravelLogApp.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', main, name='main'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)