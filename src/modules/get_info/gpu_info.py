import pynvml


class NVMLManager:
    """Manages global NVML initialization state."""

    _initialized = False

    @classmethod
    def start(cls):
        if cls._initialized:
            raise RuntimeError("NVML is already initialized.")

        try:
            pynvml.nvmlInit()
            cls._initialized = True
        except Exception as e:
            raise RuntimeError(f"NVML init failed: {e}") from e

    @classmethod
    def stop(cls):
        if not cls._initialized:
            return

        try:
            pynvml.nvmlShutdown()
            cls._initialized = False
        except Exception as e:
            raise RuntimeError(f"Failed to shutdown NVML: {e}")

    @staticmethod
    def is_initialized() -> bool:
        return NVMLManager._initialized


class GpuInfo:

    def __init__(self, device_index: int = 0) -> None:
        """Initialize GPU info for a specific device.
        Args:
            device_index: Index of the GPU (default: 0)
        """

        if not NVMLManager.is_initialized():
            raise RuntimeError("NVML was not initialized.")

        try:
            self._handle = pynvml.nvmlDeviceGetHandleByIndex(device_index)
            self._name: str = pynvml.nvmlDeviceGetName(self._handle)
        except Exception as e:
            raise RuntimeError(f"Failed to access GPU {device_index}: {e}") from e

    @property
    def name(self) -> str:
        """Returns the name of the GPU."""
        return self._name

    def get_temp(self) -> int:
        """Returns the GPU temperature in Celsius."""
        try:
            temp = pynvml.nvmlDeviceGetTemperature(
                self._handle, pynvml.NVML_TEMPERATURE_GPU
            )
            return temp
        except Exception as e:
            raise RuntimeError(f"Failed to get temperature: {e}") from e

    def get_fan_speed(self) -> int:
        """Returns the fan speed in RPM."""
        try:
            speed = pynvml.nvmlDeviceGetFanSpeed(self._handle)
            return speed
        except Exception as e:
            raise RuntimeError(f"Failed to get fan speed: {e}") from e

    def get_min_max_fan_speed(self):
        """Returns the fan min and max RPM"""
        try:
            min_max: list[int] = pynvml.nvmlDeviceGetMinMaxFanSpeed(self._handle)  # type: ignore

            fan_speeds: dict[str, int] = {
                "min": min_max[0],
                "max": min_max[1],
            }

            return fan_speeds

        except Exception as e:
            raise RuntimeError(f"Failed to get fan speed: {e}") from e

    def get_memory_info(self):
        """Returns the memory info in a dictionary [total, free, used]"""
        try:
            info = pynvml.nvmlDeviceGetMemoryInfo(self._handle)

            memory_info: dict[str, int] = {
                "total": info.total,
                "free": info.free,
                "used": info.used,
            }  # type: ignore

            return memory_info
        except Exception as e:
            raise RuntimeError(f"Failed to get memory info: {e}") from e

    def get_usage(self):
        """Returns the gpu usage percent info in a dictionary [gpu, memory]"""
        try:
            info = pynvml.nvmlDeviceGetUtilizationRates(self._handle)

            usage_info: dict[str, int] = {
                "gpu": info.gpu,
                "memory": info.memory,
            }  # type: ignore

            return usage_info
        except Exception as e:
            raise RuntimeError(f"Failed to get usage info: {e}") from e


def main():

    NVMLManager.start()

    gpu = GpuInfo()

    print(gpu.name)
    print(gpu.get_fan_speed())
    print(gpu.get_temp())

    print(gpu.get_memory_info())

    print(gpu.get_usage())

    print(gpu.get_min_max_fan_speed())

    NVMLManager.stop()


if __name__ == "__main__":
    main()
