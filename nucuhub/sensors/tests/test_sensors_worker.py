import concurrent.futures
import json
import time

import pytest

from nucuhub.sensors.main import SensorsWorker
from nucuhub.sensors.tests.mocks import ExactDummySensor
from tests.conftest import SKIP_SLOW_TESTS


@pytest.fixture
def sensor_worker():
    worker = SensorsWorker()
    worker._worker_loop_should_run = False
    return worker


@pytest.mark.skipif(SKIP_SLOW_TESTS, reason="Reading loop tests is slow!")
def test_reading_loop(redis_fixture, sensor_worker):
    sensor_worker.sensor_modules = [ExactDummySensor]
    sensor_worker._load_modules()

    pubsub = sensor_worker.message_broker.client.get_redis().pubsub()
    pubsub.subscribe("sensors")
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        executor.submit(sensor_worker._reading_loop)
        time.sleep(5)
        sensor_worker._reading_loop_should_run = False
        executor.shutdown()

    pubsub.get_message()
    message = pubsub.get_message()
    assert (
        message.get("data").decode()
        == '[{"sensor_id": "dummy_sensor", "name": "tests", "description": "tests", "timestamp": 0, "value": 2.22}]'
    )


@pytest.mark.skipif(SKIP_SLOW_TESTS, reason="Command loop tests is very slow!")
def test_command_loop(redis_fixture, sensor_worker):
    sensor_worker.sensor_modules = [ExactDummySensor]
    sensor_worker._load_modules()

    pubsub = sensor_worker.message_broker.client.get_redis()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(sensor_worker._command_loop)
        for i in range(3):
            pubsub.publish(
                "sensors_cmd", json.dumps({"sensor_id": "tid", "action": "disable"})
            )
            time.sleep(5)
        time.sleep(5)
        sensor_worker._command_loop_should_run = False
        executor.shutdown()

    assert sensor_worker.loaded_sensor_modules[0].is_enabled is False
