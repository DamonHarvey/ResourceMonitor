import pyqtgraph as pg
from PySide6.QtWidgets import QApplication

from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem
from pyqtgraph.graphicsItems.PlotItem.PlotItem import PlotItem
from pyqtgraph.graphicsItems.ViewBox.ViewBox import ViewBox


class Plot(pg.PlotWidget):

    def __init__(self, parent=None, background="default", plotItem=None, **kargs):
        super().__init__(parent, background, plotItem, **kargs)

        self.plot_item: PlotItem = self.getPlotItem()  # type: ignore
        self.view_box: ViewBox = self.plot_item.getViewBox()

        self._init_settings()

        self.curve: PlotDataItem = self.plot(pen="r")

        self.data = []

    def _init_settings(self):
        pg.setConfigOptions(antialias=True)
        self.setMouseEnabled(False, False)
        self.hideButtons()

        self.MAX_X_RANGE = 120
        self.setXRange(0, self.MAX_X_RANGE)

        self.plot_item.setMenuEnabled(False)
        self.view_box.invertX(True)

    def add_update(self, data: int | float):

        self.data.insert(0, data)

        if len(self.data) > self.MAX_X_RANGE:
            self.data.pop()

        self.curve.setData(self.data)


def main():
    app = QApplication([])

    window = Plot()

    window.show()

    window.add_update(1)

    app.exec()


if __name__ == "__main__":
    main()
