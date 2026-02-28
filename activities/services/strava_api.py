import requests
import logging
from django.conf import settings

from ..constants import EPOCH_TIMESTAMP, QUANTITY_PER_PAGE
from ..exceptions import StravaAPIError, StravaAuthenticationError, StravaRateLimitError, StravaTokenExpiredError
from .cache_service import CacheService

logger = logging.getLogger(__name__)


class StravaAPIService:
    def __init__(self, access_token: str, user_id: str = None):
        self.access_token = access_token
        self.user_id = user_id or "default"
        self.base_url = settings.STRAVA_API_BASE_URL
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def get_athlete(self) -> dict:
        response = requests.get(f"{self.base_url}/athlete", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_all_activities(self, after_timestamp: float = None, force_refresh: bool = False) -> list:
        """Obtém todas as atividades com cache"""
        if after_timestamp is None:
            after_timestamp = EPOCH_TIMESTAMP

        # Tentar obter do cache primeiro
        if not force_refresh:
            cached_activities = CacheService.get_activities(self.user_id, self.access_token)
            if cached_activities is not None:
                return cached_activities

        # Buscar da API se não estiver em cache
        logger.info("Buscando atividades da API Strava")
        all_activities = []
        page = 1
        has_error = False

        while True:
            try:
                response = requests.get(
                    f"{self.base_url}/athlete/activities",
                    headers=self.headers,
                    params={
                        "after": after_timestamp,
                        "page": page,
                        "per_page": QUANTITY_PER_PAGE,
                    },
                    timeout=30,  # Timeout de 30 segundos
                )

                if response.status_code == 401:
                    logger.error("Token expirado ou inválido")
                    raise StravaTokenExpiredError("Token de acesso expirado ou inválido")
                elif response.status_code == 429:
                    logger.warning("Rate limit atingido, aguardando...")
                    import time
                    time.sleep(2)  # Esperar 2 segundos
                    continue
                elif response.status_code >= 400:
                    error_msg = f"Erro na API: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    raise StravaAPIError(error_msg, response.status_code)
                elif response.status_code != 200:
                    logger.error(f"Erro inesperado na API: {response.status_code}")
                    raise StravaAPIError(f"Erro inesperado na API Strava", response.status_code)

                activities = response.json()
                if not activities:
                    break

                all_activities.extend(activities)
                page += 1

                # Limitar para evitar loops infinitos
                if page > 100:  # Máximo de 10.000 atividades
                    logger.warning("Limite máximo de páginas atingido")
                    break

            except requests.exceptions.Timeout as e:
                logger.error(f"Timeout na requisição: {e}")
                raise StravaAPIError("Timeout na comunicação com API Strava")
            except requests.exceptions.ConnectionError as e:
                logger.error(f"Erro de conexão: {e}")
                raise StravaAPIError("Falha na conexão com API Strava")
            except requests.exceptions.RequestException as e:
                logger.error(f"Erro de requisição: {e}")
                raise StravaAPIError(f"Erro na comunicação com API Strava: {str(e)}")
            except ValueError as e:
                logger.error(f"Erro ao processar JSON: {e}")
                raise StravaAPIError("Resposta inválida da API Strava")
            except Exception as e:
                logger.error(f"Erro inesperado: {e}")
                raise StravaAPIError(f"Erro inesperado: {str(e)}")

        # Armazenar no cache apenas se não houver erros
        if not has_error and all_activities:
            CacheService.set_activities(self.user_id, self.access_token, all_activities)
        elif has_error and not all_activities:
            # Tentar usar cache antigo como fallback
            cached_activities = CacheService.get_activities(self.user_id, self.access_token)
            if cached_activities:
                return cached_activities

        return all_activities
