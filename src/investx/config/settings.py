"""Application settings with Pydantic Settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "INVESTX_"}

    bcb_base_url: str = "https://api.bcb.gov.br/dados/serie/bcdata.sgs"
    bcb_timeout_seconds: float = 10.0
    bcb_max_retries: int = 2

    # Fallback rates (annual %) used when BCB API is unreachable
    fallback_selic: float = 14.25
    fallback_cdi: float = 14.15
    fallback_ipca: float = 5.49
    fallback_poupanca: float = 7.40
    fallback_tr: float = 0.10


settings = Settings()
