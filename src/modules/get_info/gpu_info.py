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

    def get_min_fan_speed(self):
        """Returns min fan speed"""
        try:
            fan_speed: list[int] = pynvml.nvmlDeviceGetMinMaxFanSpeed(self._handle)  # type: ignore

            return fan_speed[0]

        except Exception as e:
            raise RuntimeError(f"Failed to get fan speed: {e}") from e

    def get_max_fan_speed(self):
        """Returns max fan speed"""
        try:
            fan_speed: list[int] = pynvml.nvmlDeviceGetMinMaxFanSpeed(self._handle)  # type: ignore

            return fan_speed[1]

        except Exception as e:
            raise RuntimeError(f"Failed to get fan speed: {e}") from e

    def get_total_memory(self):
        """Returns total memory"""
        try:
            memory_info = pynvml.nvmlDeviceGetMemoryInfo(self._handle)

            return int(memory_info.total)  # type: ignore
        except Exception as e:
            raise RuntimeError(f"Failed to get memory info: {e}") from e

    def get_free_memory(self):
        """Returns free memory"""
        try:
            memory_info = pynvml.nvmlDeviceGetMemoryInfo(self._handle)

            return int(memory_info.free)  # type: ignore
        except Exception as e:
            raise RuntimeError(f"Failed to get memory info: {e}") from e

    def get_used_memory(self):
        """Returns used memory"""
        try:
            memory_info = pynvml.nvmlDeviceGetMemoryInfo(self._handle)

            return int(memory_info.used)  # type: ignore
        except Exception as e:
            raise RuntimeError(f"Failed to get memory info: {e}") from e

    def get_memory_usage(self):
        """Returns the memory usage percent"""
        try:
            usage_info = pynvml.nvmlDeviceGetUtilizationRates(self._handle)

            return int(usage_info.memory)  # type: ignore
        except Exception as e:
            raise RuntimeError(f"Failed to get usage info: {e}") from e

    def get_gpu_usage(self):
        """Returns the gpu usage percent"""
        try:
            usage_info = pynvml.nvmlDeviceGetUtilizationRates(self._handle)

            return int(usage_info.gpu)  # type: ignore
        except Exception as e:
            raise RuntimeError(f"Failed to get usage info: {e}") from e


def main():

    NVMLManager.start()

    gpu = GpuInfo()

    print(gpu.name)
    print(gpu.get_fan_speed())
    print(gpu.get_temp())

    print(gpu.get_total_memory())
    print(gpu.get_used_memory())
    print(gpu.get_free_memory())

    print(gpu.get_memory_usage())
    print(f"gpu: {gpu.get_gpu_usage()}")

    print(gpu.get_min_fan_speed())
    print(gpu.get_max_fan_speed())

    NVMLManager.stop()


if __name__ == "__main__":
    main()
