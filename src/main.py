from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget
from PySide6.QtCore import QSize, QTimer, Qt

from modules.get_info import gpu_info

from modules.plot.plotting import Plot


class Grapher(QMainWindow):

    def __init__(self):
        super().__init__()

        self.plot_widget = Plot()

        self.gpu = gpu_info.GpuInfo()

        self.setCentralWidget(self.plot_widget)

        self._init_timer()

    def _init_timer(self):
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.do_update)
        self.timer.start()

    def do_update(self) -> None:

        info = self.gpu.get_memory_info()["used"] / (1024**3)

        self.plot_widget.add_update(info)


def main():

    gpu_info.NVMLManager.start()

    app = QApplication([])

    window = Grapher()

    window.show()
    app.exec()

    gpu_info.NVMLManager.stop()


if __name__ == "__main__":
    main()
