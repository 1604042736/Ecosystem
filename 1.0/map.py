from random import randint
from Other.ground import Ground

from Other.water import Water
from Plant.grass import Grass


class Map(list):
    '''地图'''

    def __init__(self, *args):
        super().__init__(*args)
        self.camera = [0, 0]  # 摄像机
        self.count = {}  # 计数

    def add_entity(self, entity):
        '''添加实体'''
        x, y = entity.x, entity.y
        self[x][y].append(entity)

        name = entity.__class__.__name__
        if name not in self.count:
            self.count[name] = 0
        self.count[name] += 1

    def del_entity(self, entity):
        '''删除实体'''
        x, y = entity.x, entity.y
        self[x][y].remove(entity)

        name = entity.__class__.__name__
        self.count[name] -= 1

    def move_entity(self, entity, x, y):
        '''移动实体'''
        self.del_entity(entity)
        entity.x, entity.y = x, y
        self.add_entity(entity)

    def has_entity(self, entity, x, y):
        '''在(x,y)中是否有entity'''
        try:
            for i in self[x][y]:
                if isinstance(i, entity):
                    return True
        except IndexError:
            pass
        return False

    def create_world(self):
        '''创建世界'''
        for x, i in enumerate(self):
            for y, j in enumerate(i):
                if not randint(0, 5) and x != 0 and y != 0:
                    Water(x, y)
                else:
                    if not randint(0, 3):
                        Grass(x, y)
                    else:
                        Ground(x, y)

    def get_obs(self, obs=(Water,)):
        '''获得障碍物的位置'''
        result = []
        # 遍历地图找到障碍
        for ix, x in enumerate(self):
            for iy, y in enumerate(x):
                for e in y:
                    for o in obs:
                        if isinstance(e, o):
                            result.append((ix, iy))
                            break
                    else:
                        continue
                    break
        return result
