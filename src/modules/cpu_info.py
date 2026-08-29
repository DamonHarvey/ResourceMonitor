import psutil


class CpuInfo:

    def __init__(self) -> None:
        pass

    def get_usage(self):

        usage = psutil.cpu_percent()

        return usage


def main():

    cpu = CpuInfo()


if __name__ == "__main__":
    main()
