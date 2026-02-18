from django.http import JsonResponse
from django.shortcuts import redirect, render

from .services import StatisticsService, StravaAPIService, StravaAuthService


def _get_strava_session(request) -> dict | None:
    auth_service = StravaAuthService()
    session_data = {
        "access_token": request.session.get("access_token"),
        "refresh_token": request.session.get("refresh_token"),
        "expires_at": request.session.get("expires_at"),
    }

    valid_token = auth_service.get_valid_token(session_data)

    if valid_token and valid_token != session_data:
        request.session["access_token"] = valid_token.get("access_token")
        request.session["refresh_token"] = valid_token.get("refresh_token")
        request.session["expires_at"] = valid_token.get("expires_at")

    return valid_token


def _is_authenticated(request) -> bool:
    return _get_strava_session(request) is not None


def index(request):
    if _is_authenticated(request):
        return redirect("activities:dashboard")

    return render(request, "activities/index.html")


def strava_login(request):
    auth_service = StravaAuthService()
    auth_url = auth_service.get_authorization_url()
    return redirect(auth_url)


def strava_callback(request):
    code = request.GET.get("code")
    error = request.GET.get("error")

    if error:
        return render(request, "activities/error.html", {"error": error})

    if not code:
        return render(request, "activities/error.html", {"error": "Código de autorização não recebido"})

    try:
        auth_service = StravaAuthService()
        token_data = auth_service.exchange_code_for_token(code)

        request.session["access_token"] = token_data.get("access_token")
        request.session["refresh_token"] = token_data.get("refresh_token")
        request.session["expires_at"] = token_data.get("expires_at")

        athlete = token_data.get("athlete", {})
        request.session["athlete_name"] = f"{athlete.get('firstname', '')} {athlete.get('lastname', '')}".strip()
        request.session["athlete_profile"] = athlete.get("profile")

        return redirect("activities:dashboard")

    except Exception as e:
        return render(request, "activities/error.html", {"error": str(e)})


def strava_logout(request):
    request.session.flush()
    return redirect("activities:index")


def dashboard(request):
    session_data = _get_strava_session(request)

    if not session_data:
        return redirect("activities:index")

    try:
        api_service = StravaAPIService(session_data["access_token"])
        activities = api_service.get_all_activities()

        stats_service = StatisticsService(activities)

        context = {
            "athlete_name": request.session.get("athlete_name", "Atleta"),
            "athlete_profile": request.session.get("athlete_profile"),
            "general_stats": stats_service.get_general_statistics(),
            "monthly_stats": stats_service.get_monthly_statistics(),
            "activity_type_stats": stats_service.get_activity_type_statistics(),
            "weekly_stats": stats_service.get_weekly_statistics(),
            "sport_types": stats_service.get_sport_types(),
            "all_activities": stats_service.get_all_activities(),
        }

        return render(request, "activities/dashboard.html", context)

    except Exception as e:
        return render(request, "activities/error.html", {"error": str(e)})


def activities_by_sport(request, sport_type: str):
    session_data = _get_strava_session(request)

    if not session_data:
        return JsonResponse({"error": "Não autenticado"}, status=401)

    try:
        api_service = StravaAPIService(session_data["access_token"])
        activities = api_service.get_all_activities()

        stats_service = StatisticsService(activities)
        filtered_activities = stats_service.get_activities_by_sport_type(sport_type)

        return JsonResponse({"activities": filtered_activities})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
