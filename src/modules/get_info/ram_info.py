import psutil


class RamInfo:

    def __init__(self) -> None:
        pass

    def get_usage(self):
        return psutil.virtual_memory().percent

    def get_ram_info(self):

        info = psutil.virtual_memory()

        memory_info: dict[str, int] = {
            "total": info.total,
            "free": info.free,
            "used": info.used,
        }

        return memory_info


def main():

    ram = RamInfo()


if __name__ == "__main__":
    main()
