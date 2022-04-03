from entity import *
import globals


class Ground(Entity):
    '''地面'''

    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.image = globals.texture.replace_color(
            0, (255, 0, 255), (109, 88, 85))
