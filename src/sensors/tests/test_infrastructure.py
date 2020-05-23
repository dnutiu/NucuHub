import json

import pytest

from src.sensors.infrastructure import Database, Messaging


@pytest.mark.parametrize(
    "message_data",
    [
        pytest.param({}, id="empty-data"),
        pytest.param({"sensor": "test", "data": "test"}, id="normal-data"),
        pytest.param(
            {"sensor": "test", "temp": 22.0, "calibrated": True}, id="normal-data"
        ),
    ],
)
def test_messaging_publish(redis_fixture, message_data):
    pub_sub = redis_fixture.get_redis().pubsub()
    pub_sub.subscribe("sensors")

    messaging = Messaging()
    messaging.publish(message_data)

    pub_sub.get_message()
    message = pub_sub.get_message()

    assert json.loads(message["data"]) == message_data


def test_database_save(redis_fixture):
    redis_cli = redis_fixture.get_redis()
    database = Database()
    database.save_config("test_config", {"test_data": 1})
    data = redis_cli.get("test_config")
    assert data.decode() == '{"test_data": 1}'


def test_database_load(redis_fixture):
    database = Database()
    database.save_config("test_config", {"test_data": 1})
    database = database.load_config("test_config")
    assert database == {"test_data": 1}
