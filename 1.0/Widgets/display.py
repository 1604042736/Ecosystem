from threading import Thread
import time
from Widgets.generec import GeneRec
from Widgets.statistics import *
import globals
from Widgets.basewidget import *


class Display(BaseWidget):
    '''绘制地图'''

    def __init__(self) -> None:
        super().__init__()
        self.resize(1000, 618)
        self.setWindowTitle('地图')

        self.statistics = Statistics()
        self.pb_statistics = QPushButton(self, text='统计信息')
        self.pb_statistics.setGeometry(0, 0, 64, 32)
        self.pb_statistics.clicked.connect(self.on_pb_statistics_clicked)

        globals.generec = GeneRec()
        self.pb_generec = QPushButton(self, text='基因记录')
        self.pb_generec.setGeometry(0, 32, 64, 32)
        self.pb_generec.clicked.connect(self.on_pb_generec_clicked)

        self.t_width, self.t_height = 16, 16  # 贴图的长宽

        self.map = globals.map

        self._t = Thread(target=self.display)
        self._t.setDaemon(True)
        self._t.start()

    def on_pb_statistics_clicked(self):
        self.statistics.show()

    def on_pb_generec_clicked(self):
        globals.generec.show()

    def paintEvent(self, a0):
        qp = QPainter()
        qp.begin(self)

        c_x, c_y = self.map.camera

        # 将窗口根据贴图长宽划分
        gamewidth = int(self.width()/self.t_width)
        gameheight = int(self.height()/self.t_height)
        halfgamewidth = int(gamewidth/2)
        halfgameheight = int(gameheight/2)
        halfrealwidth = halfgamewidth*self.t_width
        halfrealheight = halfgameheight*self.t_height

        # 计算将要绘制的左上角方块
        minx = c_x-halfgamewidth
        miny = c_y-halfgameheight

        # 计算右下角方块位置
        maxx = c_x+halfgamewidth
        maxy = c_y+halfgameheight

        # 绘制这个区间的方块
        for x in range(minx, maxx+1):
            for y in range(miny, maxy+1):
                if x < 0 or y < 0:
                    continue
                try:
                    for i in self.map[x][y]:
                        # 计算与摄像机的相对位置
                        _x = c_x-x
                        _y = c_y-y
                        if i.image:
                            qp.drawImage(QRect(halfrealwidth-_x*self.t_width, halfrealheight -
                                               _y*self.t_height, self.t_width, self.t_height), i.image)
                except IndexError:
                    pass

        qp.end()

    def keyPressEvent(self, a0) -> None:
        if a0.key() == Qt.Key_L:
            self.map.camera[0] += 1
        elif a0.key() == Qt.Key_J:
            self.map.camera[0] -= 1
        elif a0.key() == Qt.Key_I:
            self.map.camera[1] -= 1
        elif a0.key() == Qt.Key_K:
            self.map.camera[1] += 1
        super().keyPressEvent(a0)

    def display(self):
        while True:
            globals.time += 1
            self.update()
            time.sleep(globals.wait)
