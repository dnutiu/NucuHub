import pytest

from src.domain.config import ApplicationConfig
from src.infrastructure.redis import RedisService


@pytest.fixture
def redis_fixture():
    ApplicationConfig.REDIS_URL = "localhost"
    RedisService.set_singleton(None)
    redis = RedisService.instance()
    return redis