from plant import *
import globals


class Grass(Plant):
    '''草'''

    def __init__(self, x, y, gene=[]) -> None:
        super().__init__(x, y, gene)
        self.image = globals.texture.replace_color(
            6, (255, 255, 255), (0, 255, 0))
