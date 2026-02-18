"""Exceções customizadas para o app activities"""


class StravaAPIError(Exception):
    """Erro na API Strava"""
    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class StravaAuthenticationError(StravaAPIError):
    """Erro de autenticação Strava"""
    def __init__(self, message: str = "Falha na autenticação com Strava"):
        super().__init__(message, 401)


class StravaRateLimitError(StravaAPIError):
    """Erro de rate limit da API Strava"""
    def __init__(self, message: str = "Limite de requisições excedido"):
        super().__init__(message, 429)


class StravaTokenExpiredError(StravaAPIError):
    """Token Strava expirado"""
    def __init__(self, message: str = "Token de acesso expirado"):
        super().__init__(message, 401)


class DataProcessingError(Exception):
    """Erro no processamento de dados"""
    pass


class CacheError(Exception):
    """Erro no sistema de cache"""
    pass
