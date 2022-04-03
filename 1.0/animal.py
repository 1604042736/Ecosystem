from ctypes.wintypes import tagRECT
from itertools import count
from random import randint
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
        self.max_hungry = 1000
        self.max_thirty = 1000

        self.speed = 10  # 速度,也是每个循环等待的时间

        self.reproduction_wish = 0  # 生殖欲望
        self.max_reproduction_wish = 50  # 最大生殖欲望
        self.reproduction_num = 5  # 一次繁殖可以生的数量
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
        # 确立每次移动的方向
        t = self.x-x
        if t > 0:
            dx = -1
        elif t == 0:
            dx = 0
        elif t < 0:
            dx = 1
        t = self.y-y
        if t > 0:
            dy = -1
        elif t == 0:
            dy = 0
        elif t < 0:
            dy = 1

        cm = self.check_move(x, y)

        while True:
            m = self.move(dx, dy)
            if not m:  # 被阻挡
                self.rand_move()
            if cm:  # 可以直接到达
                if self.x == x:
                    dx = 0
                if self.y == y:
                    dy = 0
            else:  # 不可以直接到达就到旁边
                for i in (1, 0, -1):
                    for j in (1, 0, -1):
                        if self.x == x+i:
                            dx = 0
                        if self.y == y+j:
                            dy = 0
            if dx == dy == 0:
                break
            yield  # 作为一个迭代器

    def reproduction(self):
        '''生殖'''
        a = self.get_insight(self.__class__)
        if a:  # 找到同类
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
