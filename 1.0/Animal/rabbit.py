from Other.water import Water
from Plant.grass import Grass
from animal import *
import globals
import time


class Rabbit(Animal):
    '''兔子'''

    def __init__(self, x, y, gene=[]) -> None:
        super().__init__(x, y, gene)
        self.image = globals.texture.replace_color(
            82, (255, 0, 255), (0, 0, 0))

    def one_step(self):
        d_thirty = self.thirty-self.safe_thirty  # 相差的口渴度
        d_hungry = self.hungry-self.safe_hungry  # 相差的饥饿度
        if not (d_thirty <= 0 and d_hungry <= 0):
            # 选择最需要的进行
            d_thirty = self.max_thirty-self.thirty
            d_hungry = self.max_hungry-self.hungry
            if d_thirty < d_hungry:
                water = self.get_nearest_sight(Water)
                if water:  # 找到水
                    self.add_todo(self.move_toward(
                        water.x, water.y), self.while_todrink, self.after_todrink, water)
            else:
                food = self.get_nearest_sight(Grass)
                if food:
                    self.add_todo(self.move_toward(food.x, food.y),
                                  self.while_toeat, self.after_toeat, food)
        super().one_step()

    def while_toeat(self, iter, target):
        '''正在去吃的路上'''
        if target.die:  # 要吃的目标消失
            self.remove_todo(iter)

    def after_toeat(self, iter, target):
        '''来到了食物旁'''
        if not target.die:
            self.hungry -= self.sub_hungry
            if self.hungry < 0:
                self.hungry = 0
            target.kill()

    def while_todrink(self, iter, target):
        '''去水源的路上'''

    def after_todrink(self, iter, target):
        '''来到水源旁'''
        self.thirty -= self.sub_thirty
        if self.thirty < 0:
            self.thirty = 0
