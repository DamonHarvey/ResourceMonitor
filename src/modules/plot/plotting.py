import pyqtgraph as pg
from PySide6.QtWidgets import QApplication

from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem
from pyqtgraph.graphicsItems.PlotItem.PlotItem import PlotItem
from pyqtgraph.graphicsItems.ViewBox.ViewBox import ViewBox


class Plot(pg.PlotWidget):

    def __init__(self):
        super().__init__()

        self.init_graph_specifications()

        self._init_settings()

        self.curve: PlotDataItem = self.plot(pen="r")

        self.data = []

        self.max_x = 10

    def _init_settings(self):
        pg.setConfigOptions(antialias=True)

        self.setMouseEnabled(False, False)
        self.hideButtons()
        self.plotItem.setMenuEnabled(False)  # type: ignore

        self.plotItem.getViewBox().invertX(True)  # type: ignore

    def init_graph_specifications(self):
        self.set_max_x_range()
        self.set_max_y_range()

    def set_max_x_range(self, max_x_range: int | float | None = None):
        if max_x_range is None:
            self.enableAutoRange(axis="x")
        else:
            self.setXRange(max_x_range, 0)

            self.max_x = int(self.getViewBox().viewRange()[0][1])

    def set_max_y_range(self, max_y_range: int | float | None = None):
        if max_y_range is None:
            self.enableAutoRange(axis="y")
        else:
            self.setYRange(max_y_range, 0)

    def update_data(self, data: int | float):

        self.data.insert(0, data)

        if len(self.data) > self.max_x:
            self.data.pop()

        self.curve.setData(self.data)


def main():
    app = QApplication([])

    window = Plot()

    window.set_max_y_range(100)
    window.set_max_x_range(25)

    for i in range(100):
        window.update_data(i)

    window.show()
    app.exec()


if __name__ == "__main__":
    main()
