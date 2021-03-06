import typing

from nucuhub import utils

from nucuhub.sensors.types import (  # isort:skip
    SensorConfig,
    SensorMeasurement,
    SensorModule,
    SensorState,
)


class CpuTemperature(SensorModule):
    sensor_id = "cpu_temperature_sensor"
    file_name = "/sys/class/thermal/thermal_zone0/temp"

    def _configure(self) -> SensorConfig:
        return SensorConfig(
            id=self.sensor_id,
            name="Cpu Temp",
            description="Outputs the CPU temperature in celsius",
            enabled=True,
        )

    def _get_data(self) -> typing.List[SensorMeasurement]:
        try:
            with open(self.file_name) as fd:
                data = fd.readline()
            return [
                SensorMeasurement(
                    sensor_id=self.sensor_id,
                    name="thermal_zone0",
                    description="CPU package temperature in celsius",
                    value=float(data) / 1000,
                    timestamp=utils.get_now_timestamp(),
                )
            ]
        except IOError as e:
            self.set_state(SensorState.ERROR)
            self.disable()
            self._logger.error(f"CpuTemperatureSensor: {e}")
            return []
