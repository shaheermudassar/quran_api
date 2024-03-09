# api/urls.py

from django.urls import path
from .views import CompareAudioFiles, form

urlpatterns = [
    path('', form, name='form'),
    path('compare-audio/', CompareAudioFiles.as_view(), name='compare-audio'),
]
