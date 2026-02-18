from django.urls import path

from . import views

app_name = "activities"

urlpatterns = [
    path("", views.index, name="index"),
    path("auth/login/", views.strava_login, name="strava_login"),
    path("auth/callback/", views.strava_callback, name="strava_callback"),
    path("auth/logout/", views.strava_logout, name="strava_logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("api/activities/<str:sport_type>/", views.activities_by_sport, name="activities_by_sport"),
]
