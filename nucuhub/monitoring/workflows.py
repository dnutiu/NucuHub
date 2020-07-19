import nucuhub.monitoring.infrastructure as infrastructure
from nucuhub.logging import get_logger
from nucuhub.monitoring import ConsumerStage

logger = get_logger("MonitoringWorkflows")


class DebugWorkflow(ConsumerStage):
    name = "DebugWorkflow"

    def process(self, message):
        logger.debug(f"DebugWorkflow {message}")
        return False


class SensorsWorkflow(ConsumerStage):
    name = "SensorsWorkflow"

    def process(self, message):
        """
            Processes message of the type:
            Example message: {'type': 'message', 'pattern': None, 'channel': b'sensors', 'data': b'test'}
        :param message:
        """
        type = message.get("type")
        channel = message.get("channel", "").decode()
        stop = False
        if type == "message" and channel == "sensors":
            data = infrastructure.Messaging.decode_message_data(message)
            db = infrastructure.Firebase.instance()
            db.save("sensors", data)
            stop = True
        return stop
