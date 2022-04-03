from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class BaseWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

    def show(self) -> None:
        '''捕获show,将widget给mainwindow管理,close与之类似'''
        import globals
        if globals.mainwindow != None and globals.mainwindow.isVisible():
            globals.mainwindow.catchwidget(self)
            return
        return super().show()

    def close(self) -> bool:
        import globals
        if globals.mainwindow != None:
            globals.mainwindow.closewidget(self)
        return super().close()

    def keyPressEvent(self, a0) -> None:
        if a0.key() == Qt.Key_B:  # 按B将窗体重新加入mainwindow
            self.backtomainwin()
        elif a0.key() == Qt.Key_S:  # 按S将窗体分离
            import globals
            if globals.mainwindow != None and globals.mainwindow.isVisible():
                globals.mainwindow.sepwidget(self)
        elif a0.key() == Qt.Key_D:  # 按D回到上一个窗体
            import globals
            if globals.mainwindow != None and globals.mainwindow.isVisible():
                globals.mainwindow.closewidget(self)

    def backtomainwin(self):
        '''重回mainwindow'''
        self.show()
