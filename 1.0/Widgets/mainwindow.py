from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Widgets.display import *


class MainWindow(QStackedWidget):
    '''对程序中的窗体进行管理'''

    def __init__(self) -> None:
        super().__init__()
        self.resize(1000, 618)
        self.setWindowTitle('生态系统')

    def ready(self):
        '''准备好后'''
        self.display = Display()
        self.display.show()

    def catchwidget(self, widget):
        '''捕获窗体'''
        self.addWidget(widget)
        self.setCurrentIndex(self.count()-1)

    def closewidget(self, widget):
        '''删除窗体'''
        self.removeWidget(widget)

    def sepwidget(self, widget):
        '''独立窗口'''
        self.closewidget(widget)
        widget.setParent(None)
        QWidget.show(widget)

    def keyPressEvent(self, a0) -> None:
        self.currentWidget().keyPressEvent(a0)  #向当前窗口传递
