import hashlib
import logging
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)


class CacheService:
    """Serviço centralizado para gerenciamento de cache"""
    
    @staticmethod
    def get_cache_key(prefix: str, *args) -> str:
        """Gera chave de cache única baseada em prefixo e argumentos"""
        key_data = ":".join(str(arg) for arg in args)
        key_hash = hashlib.md5(key_data.encode()).hexdigest()
        return f"strava_stats:{prefix}:{key_hash}"
    
    @staticmethod
    def get_activities(user_id: str, access_token: str):
        """Recupera atividades do cache"""
        cache_key = CacheService.get_cache_key("activities", user_id, access_token[:10])
        return cache.get(cache_key)
    
    @staticmethod
    def set_activities(user_id: str, access_token: str, activities: list):
        """Armazena atividades no cache"""
        cache_key = CacheService.get_cache_key("activities", user_id, access_token[:10])
        try:
            cache.set(cache_key, activities, timeout=settings.CACHE_TIMEOUT_ACTIVITIES)
            logger.info(f"Atividades cacheadas para usuário {user_id}")
        except Exception as e:
            logger.error(f"Erro ao cachear atividades: {e}")
    
    @staticmethod
    def get_stats(user_id: str, stats_type: str):
        """Recupera estatísticas do cache"""
        cache_key = CacheService.get_cache_key("stats", user_id, stats_type)
        return cache.get(cache_key)
    
    @staticmethod
    def set_stats(user_id: str, stats_type: str, stats_data: dict):
        """Armazena estatísticas no cache"""
        cache_key = CacheService.get_cache_key("stats", user_id, stats_type)
        try:
            cache.set(cache_key, stats_data, timeout=settings.CACHE_TIMEOUT_STATS)
            logger.info(f"Estatísticas {stats_type} cacheadas para usuário {user_id}")
        except Exception as e:
            logger.error(f"Erro ao cachear estatísticas {stats_type}: {e}")
    
    @staticmethod
    def invalidate_user_cache(user_id: str):
        """Invalida todo o cache de um usuário"""
        try:
            # Em produção, poderíamos usar cache.delete_many com pattern matching
            # Por ora, limpamos o cache completamente
            cache.clear()
            logger.info(f"Cache invalidado para usuário {user_id}")
        except Exception as e:
            logger.error(f"Erro ao invalidar cache do usuário {user_id}: {e}")
