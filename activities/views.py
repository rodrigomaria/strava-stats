from django.http import JsonResponse
from django.shortcuts import redirect, render
import logging

from .services import StatisticsService, StravaAPIService, StravaAuthService
from .exceptions import StravaAPIError, StravaAuthenticationError, StravaTokenExpiredError

logger = logging.getLogger(__name__)


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

    except StravaAuthenticationError as e:
        logger.error(f"Erro de autenticação Strava: {e}")
        return render(request, "activities/error.html", {"error": f"Erro de autenticação: {e}"})
    except Exception as e:
        logger.error(f"Erro inesperado no callback Strava: {e}", exc_info=True)
        return render(request, "activities/error.html", {"error": "Erro ao processar autenticação com Strava"})


def strava_logout(request):
    request.session.flush()
    return redirect("activities:index")


def dashboard(request):
    session_data = _get_strava_session(request)

    if not session_data:
        return redirect("activities:index")

    try:
        # Usar user_id da sessão para cache
        user_id = request.session.get("athlete_name", "anonymous") or "default"
        api_service = StravaAPIService(session_data["access_token"], user_id)
        activities = api_service.get_all_activities()

        stats_service = StatisticsService(activities, user_id)

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

    except StravaTokenExpiredError as e:
        logger.error(f"Token Strava expirado: {e}")
        # Limpar sessão e redirecionar para login
        request.session.flush()
        return render(request, "activities/error.html", {"error": "Sua sessão expirou. Por favor, faça login novamente."})
    except StravaAPIError as e:
        logger.error(f"Erro na API Strava: {e}")
        return render(request, "activities/error.html", {"error": f"Erro ao carregar dados do Strava: {e}"})
    except Exception as e:
        logger.error(f"Erro inesperado no dashboard: {e}", exc_info=True)
        return render(request, "activities/error.html", {"error": "Erro ao carregar o dashboard"})


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

    except StravaAPIError as e:
        logger.error(f"Erro na API Strava: {e}")
        return JsonResponse({"error": f"Erro ao carregar atividades: {e}"}, status=500)
    except Exception as e:
        logger.error(f"Erro inesperado ao filtrar atividades: {e}", exc_info=True)
        return JsonResponse({"error": "Erro ao processar solicitação"}, status=500)
