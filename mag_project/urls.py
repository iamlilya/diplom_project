from django.contrib import admin
from django.urls import include, path

from ilmirapp import views
from rest_framework.response import Response
from rest_framework.views import APIView

class Gradient(APIView):
    def get(self, request):
        print(request.GET)
        latitude = request.GET['latitude']
        longitude = request.GET['longitude']
        response = "latitude: " + latitude + "; longitude: " + longitude
        return Response(response)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", views.index),
    path('api/gradient/', Gradient.as_view())
]