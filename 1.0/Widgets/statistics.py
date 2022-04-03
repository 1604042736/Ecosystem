import time
from Widgets.basewidget import *
from entity import Entity
import globals
from PyQt5.QtChart import *


class Statistics(BaseWidget):
    '''统计'''
    count = 0  # 计数

    def __init__(self) -> None:
        super().__init__()
        self.resize(1000, 618)
        self.setWindowTitle('统计')

        self.charts = {}  # 图表
        self.maxy = 0  # 最大的y坐标

        self.chart_view = QChartView(self)
        self.chart_view.setGeometry(0, 0, 1000, 618)

        self.x_Aix = QValueAxis()  # 定义x轴，实例化
        self.x_Aix.setLabelFormat("%d")  # 设置坐标轴坐标显示方式，精确到小数点后两位
        self.x_Aix.setTickCount(6)  # 设置x轴有几个量程
        self.x_Aix.setMinorTickCount(0)  # 设置每个单元格有几个小的分级

        self.y_Aix = QValueAxis()  # 定义y轴
        self.y_Aix.setLabelFormat("%d")
        self.y_Aix.setTickCount(7)
        self.y_Aix.setMinorTickCount(0)

        self.chart_view.chart().setAxisX(self.x_Aix)  # 设置x轴属性
        self.chart_view.chart().setAxisY(self.y_Aix)  # 设置y轴属性

        self._t = ThreadStatistics()
        self._t.statistics.connect(self.statistics)
        self._t.start()

    def set_asis(self):
        '''设置坐标轴以达到自适应目的'''
        self.x_Aix.setRange(0, Statistics.count)  # 设置量程
        self.y_Aix.setRange(0, self.maxy)

    def statistics(self, key, val):
        '''统计'''
        if key not in self.charts:
            self.charts[key] = QLineSeries()
            self.chart_view.chart().addSeries(self.charts[key])
            self.charts[key].setName(key)
            self.set_asis()
            self.charts[key].attachAxis(self.x_Aix)
            self.charts[key].attachAxis(self.y_Aix)
        self.maxy = max(self.maxy, val)
        self.charts[key].append(QPoint(Statistics.count, val))
        self.set_asis()

    def resizeEvent(self, a0) -> None:
        self.chart_view.resize(self.width(), self.height())


class ThreadStatistics(QThread):
    '''实时统计'''
    statistics = pyqtSignal(str, int)

    def run(self):
        while True:
            for key in list(globals.map.count.keys()):
                val = globals.map.count[key]
                self.statistics.emit(key, val)
            Statistics.count += 1
            time.sleep(globals.wait*100)
