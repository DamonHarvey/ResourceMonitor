import pyqtgraph as pg
from PySide6.QtWidgets import QApplication


from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem
from pyqtgraph.graphicsItems.PlotItem.PlotItem import PlotItem
from pyqtgraph.graphicsItems.ViewBox.ViewBox import ViewBox
from pyqtgraph.graphicsItems.AxisItem import AxisItem


class Plot:

    def __init__(self):

        self._root = pg.PlotWidget()

        self._plot_item = self._get_plot_item()
        self._view_box = self._get_view_box()
        self._legend = self._get_created_legend()

        self._init_graph_specifications()
        self._init_settings()
        self._setup_legend()

        self._curve: PlotDataItem = self._plot_item.plot()

        self._legend_add_value()

        self._data = []

        self._max_x = 10

        self.set_title("None")
        self.set_x_lable("X-Axis")
        self.set_y_label("Y-Axis")
        self.set_plot_color("#ffffff")

    def _get_plot_item(self):

        plot_item = self._root.getPlotItem()

        if not isinstance(plot_item, PlotItem):
            raise TypeError

        return plot_item

    def _get_view_box(self):

        view_box = self._get_plot_item().getViewBox()

        return view_box

    def _get_created_legend(self):

        legend = self._plot_item.addLegend()

        return legend

    def _setup_legend(self):

        self._legend.mouseDragEvent = (
            lambda *args, **kwargs: None
        )  # Disables drag event

        self._legend.setOffset(0)

    def _legend_add_value(self):

        self._legend.addItem(self._curve, "Test")

    def _init_settings(self):
        pg.setConfigOptions(antialias=True)

        self._plot_item.setMenuEnabled(False)
        self._plot_item.hideButtons()

        self._view_box.setMouseEnabled(False, False)
        self._view_box.invertX(True)

    def _init_graph_specifications(self):
        self.set_max_x_range()
        self.set_max_y_range()

    def set_title(self, title: str):

        self._plot_item.setTitle(title)

    def set_x_lable(self, lable: str):

        x_axis: AxisItem = self._plot_item.getAxis("bottom")

        x_axis.setLabel(lable)

    def set_y_label(self, label: str):

        y_axis: AxisItem = self._plot_item.getAxis("left")

        y_axis.setLabel(label)

    def set_plot_color(self, color: str):

        self._curve.setPen(color)

    def set_max_x_range(self, max_x_range: int | float | None = None):
        if max_x_range is None:
            self._view_box.enableAutoRange(axis="x")

        else:
            self._view_box.setXRange(0, max_x_range, 0)

            self._max_x = int(self._view_box.viewRange()[0][1])

    def set_max_y_range(self, max_y_range: int | float | None = None):
        if max_y_range is None:
            self._view_box.enableAutoRange(axis="y")
        else:
            self._view_box.setYRange(max_y_range, 0)

    def update_data(self, data: int | float):

        self._data.insert(0, data)

        if len(self._data) > self._max_x:
            self._data.pop()

        self._curve.setData(self._data)

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
