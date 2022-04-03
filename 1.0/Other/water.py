from entity import *
import globals


class Water(Entity):
    '''水'''

    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.image = globals.texture.replace_color(
            0, (255, 0, 255), (0, 0, 255))
