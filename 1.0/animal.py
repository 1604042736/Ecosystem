from ctypes.wintypes import tagRECT
from itertools import count
from random import randint
import time
from Algorithm.pathfinding import find_path
from Other.water import Water
from creature import *
from threading import Thread
import globals


class Animal(Creature):
    '''动物'''

    def __init__(self, x, y, gene=[]) -> None:
        super().__init__(x, y, gene)

        # 基因名称
        self.gene_name = ['add_thirty',
                          'add_hungry',
                          'safe_thirty',
                          'safe_hungry',
                          'sub_thirty',
                          'sub_hungry',
                          'max_thirty',
                          'max_hungry',
                          'reproduction_wish',
                          'max_reproduction_wish',
                          'speed',
                          'reproduction_num']

        self.thirty = 0  # 口渴度
        self.hungry = 0  # 饥饿度

        self.sight = 5  # 视野
        # 运动增加的饥饿度和口渴度
        self.add_hungry = 1
        self.add_thirty = 1
        # 安全的饥饿度和口渴度,可以看成可以忍受的饥饿度和口渴度
        self.safe_hungry = 10
        self.safe_thirty = 10
        # 减少的饥饿度和口渴度
        self.sub_hungry = 100
        self.sub_thirty = 100
        # 最大的饥饿度和口渴度,超出这些会死亡
        self.max_hungry = 200
        self.max_thirty = 200

        self.speed = 10  # 速度,也是每个循环等待的时间

        self.reproduction_wish = 0  # 生殖欲望
        self.max_reproduction_wish = 50  # 最大生殖欲望
        self.reproduction_num = 3  # 一次繁殖可以生的数量
        self.reproduction_target = None  # 繁殖对象

        if gene:
            # 从基因中设置
            for i, n in enumerate(self.gene_name):
                self.__dict__[n] = gene[i]

        self._t = Thread(target=self.action)
        self._t.setDaemon(True)
        self._t.start()

    def action(self):
        '''行动'''
        while True:
            if self.die:
                break
            self.one_step()
            time.sleep(self.speed/100)

    def one_step(self):
        '''执行一步'''
        if self.thirty > self.max_thirty or self.hungry > self.max_hungry:  # 太饿或太渴会导致死亡
            self.kill()
        # 在做其他事的时侯不能繁殖
        if self.reproduction_wish > self.max_reproduction_wish and len(self.todo) == 0:
            self.reproduction_wish = 0
            self.reproduction()
        self.reproduction_wish += 1

        if self.todo:
            # 做它要做的事
            self.do_todo()
        else:
            # 随机移动
            self.rand_move()

    def get_sight(self):
        '''获取视野中的东西'''
        map = globals.map
        # TODO 将视野变成圆形
        # 矩形的视野
        # 获取左上坐标
        lx, ly = self.x-self.sight, self.y-self.sight
        if lx < 0:
            lx = 0
        if ly < 0:
            ly = 0
        # 获取右下坐标
        rx, ry = self.x+self.sight, self.y+self.sight
        if rx > len(map):
            rx = len(map)
        if ry > len(map):
            ry = len(map)
        return map[lx:rx][ly:ry]

    def get_insight(self, entity):
        '''获取在视野里的实体'''
        sight = self.get_sight()
        for i in sight:
            for j in i:
                for k in j:
                    if isinstance(k, entity):
                        return k
        return None

    def get_nearest_sight(self, entity):
        '''获取视野里最近的实体'''
        _min = 0xffff
        e = None
        sight = self.get_sight()
        for i in sight:
            for j in i:
                for k in j:
                    if isinstance(k, entity):
                        way = (k.x-self.x)**2+(k.y-self.y)**2
                        if way < _min:
                            e = k
                            _min = way
        return e

    def move(self, dx, dy):
        '''移动'''
        nx, ny = self.x+dx, self.y+dy  # 获取移动后坐标
        if self.check_move(nx, ny):  # 符合要求
            globals.map.move_entity(self, nx, ny)
            self.hungry += self.add_hungry
            self.thirty += self.add_thirty
            return True
        return False

    def check_move(self, x, y):
        '''检查移动是否合法'''
        map = globals.map
        if map.has_entity(Water, x, y):
            return False
        if x < 0 or y < 0:
            return False
        if x >= len(map) or y >= len(map):
            return False
        return True

    def rand_move(self):
        '''随机移动'''
        dx, dy = randint(-1, 1), randint(-1, 1)
        self.move(dx, dy)

    def move_toward(self, x, y):
        '''朝一个地方移动'''
        obs = globals.map.get_obs()
        move_way = find_path(
            len(globals.map), (self.x, self.y), (x, y), obs)  # 查找路径
        if move_way == None:
            return
        for _x, _y in move_way:
            dx = _x-self.x
            dy = _y-self.y
            self.move(dx, dy)
            yield

    def reproduction(self):
        '''生殖'''
        a = self.get_insight(self.__class__)
        if a and a != self:  # 找到同类(不能跟自己繁殖)
            b = a.reproduction_req(self)
            if b:  # 如果同意了
                for i in range(self.reproduction_num):
                    gene = self.inherit_gene(a.get_gene())
                    self.__class__(self.x, self.y, gene)
                # 繁殖完
                a.reproduction_target = None

    def reproduction_req(self, target):
        '''生殖请求'''
        if self.reproduction_target:  # 一次只能搞一个
            return False
        if self.hungry > self.safe_hungry or self.thirty > self.safe_thirty:
            return False
        self.reproduction_target = target
        return True

    def get_gene(self):
        '''获取基因'''
        return [self.__dict__[n] for n in self.gene_name]

    def inherit_gene(self, other_gene):
        '''基因继承'''
        self_gene = self.get_gene()
        gene = self_gene if randint(0, 1) else other_gene
        # 发生变异,几率很小
        if not randint(0, 100):
            n = randint(1, len(self_gene))  # 将要发生变异的基因个数
            for _ in range(n):
                i = randint(0, len(self_gene)-1)  # 发生变异的位置
                amount = randint(-5, 5)  # 变异数量
                gene[i] += amount
        return gene
