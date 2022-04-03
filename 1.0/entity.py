import globals


class Entity:
    '''实体'''

    def __init__(self, x, y) -> None:
        self.x, self.y = x, y
        self.image = None
        self.die = False

        globals.map.add_entity(self)

    def kill(self):
        globals.map.del_entity(self)
        self.die = True

    def __hash__(self) -> int:
        return self.__class__.__name__.__hash__()
