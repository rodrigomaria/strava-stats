from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("strava-stats/admin/", admin.site.urls),
    path("strava-stats/", include("activities.urls")),
]
