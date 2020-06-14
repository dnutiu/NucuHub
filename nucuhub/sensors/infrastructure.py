import json

from nucuhub.domain.logging import get_logger
from nucuhub.infrastructure.redis import RedisService

logger = get_logger("sensors.infrastructure")


class RedisBackend:
    client: RedisService = None

    def __init__(self):
        self.client = RedisService.instance()


class Messaging(RedisBackend):
    def __init__(self):
        super().__init__()
        self._pubsub = self.client.get_redis().pubsub()
        self._pubsub.subscribe("sensors_cmd")

    def publish(self, data):
        redis = self.client.get_redis()
        logger.debug(data)
        redis.publish("sensors", json.dumps(data))

    def get_message(self):
        try:
            message = self._pubsub.get_message(
                ignore_subscribe_messages=True, timeout=1
            )
            return json.loads(message.get("data"))
        except (TypeError, AttributeError):
            return None


class Database(RedisBackend):
    def save_config(self, name, data):
        redis = self.client.get_redis()
        redis.set(name, json.dumps(data))

    def load_config(self, name):
        redis = self.client.get_redis()
        data = redis.get(name)
        return_val = None
        if data:
            return_val = json.loads(data.decode())
        return return_val
