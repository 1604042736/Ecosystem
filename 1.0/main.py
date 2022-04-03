from pprint import pprint
import sys
from Animal.rabbit import Rabbit
import globals
from Widgets.mainwindow import *
from map import Map


def main():
    map_size = 32
    globals.map = Map([[[]for i in range(map_size)]for j in range(map_size)])
    globals.map.create_world()
    globals.map.camera = [int(map_size/2), int(map_size/2)]
    Rabbit(0, 0)
    Rabbit(1, 0)

    globals.app = QApplication(sys.argv)
    globals.mainwindow = MainWindow()
    globals.mainwindow.show()
    globals.mainwindow.ready()
    sys.exit(globals.app.exec())


if __name__ == '__main__':
    main()
