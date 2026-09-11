import pyqtgraph as pg
from PySide6.QtWidgets import QApplication


from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem
from pyqtgraph.graphicsItems.PlotItem.PlotItem import PlotItem
from pyqtgraph.graphicsItems.ViewBox.ViewBox import ViewBox


class Plot:

    def __init__(self):

        self._root = pg.PlotWidget()

        self.plot_item = self._get_plot_item()
        self.view_box = self._get_view_box()

        self.init_graph_specifications()
        self._init_settings()

        self.curve: PlotDataItem = self.plot_item.plot(pen="r")

        self.data = []

        self.max_x = 10

    def _get_plot_item(self):

        plot_item = self._root.getPlotItem()

        if not isinstance(plot_item, PlotItem):
            raise TypeError

        return plot_item

    def _get_view_box(self):

        view_box = self._get_plot_item().getViewBox()

        return view_box

    def _init_settings(self):
        pg.setConfigOptions(antialias=True)

        self.plot_item.setMenuEnabled(False)
        self.plot_item.hideButtons()
        self.plot_item.setMenuEnabled(False)

        self.view_box.invertX(True)

    def init_graph_specifications(self):
        self.set_max_x_range()
        self.set_max_y_range()

    def set_max_x_range(self, max_x_range: int | float | None = None):
        if max_x_range is None:
            self.view_box.enableAutoRange(axis="x")

        else:
            self.view_box.setXRange(0, max_x_range, 0)

            self.max_x = int(self.view_box.viewRange()[0][1])

    def set_max_y_range(self, max_y_range: int | float | None = None):
        if max_y_range is None:
            self.view_box.enableAutoRange(axis="y")
        else:
            self.view_box.setYRange(max_y_range, 0)

    def update_data(self, data: int | float):

        self.data.insert(0, data)

        if len(self.data) > self.max_x:
            self.data.pop()

        self.curve.setData(self.data)

    def widget(self):
        return self._root

    def show(self):

        self._root.show()


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
