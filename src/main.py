from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget
from PySide6.QtCore import QSize, QTimer, Qt

from modules.get_info import gpu_info

from modules.plot.plotting import Plot


class Grapher(QMainWindow):

    def __init__(self):
        super().__init__()

        self.plot_widget = Plot()

        self.gpu = gpu_info.GpuInfo()

        self.setCentralWidget(self.plot_widget.widget())

        self.init_plot_settings()
        self._init_timer()

    def _init_timer(self):
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def init_plot_settings(self):

        self.plot_widget.set_max_x_range(600)
        self.plot_widget.set_max_y_range(100)

        self.plot_widget.set_title("Gpu Usage")
        self.plot_widget.set_y_label("Usage")
        self.plot_widget.set_x_lable("Time")

        self.plot_widget.set_plot_color("#ff0000")

    def update_plot(self) -> None:

        info = self.gpu.get_gpu_usage()

        self.plot_widget.update_data(info)


def main():

    gpu_info.NVMLManager.start()

    app = QApplication([])

    window = Grapher()

    window.show()
    app.exec()

    gpu_info.NVMLManager.stop()


if __name__ == "__main__":
    main()
