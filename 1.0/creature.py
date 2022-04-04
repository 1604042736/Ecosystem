from entity import *
import globals


class Creature(Entity):
    '''生物'''

    def __init__(self, x, y, gene=[]) -> None:
        super().__init__(x, y)
        self.todo = []  # 要做的事
        self.del_todo = []  # 要删除的todo
        self.gene_name = []
        if gene and globals.generec:
            globals.generec.add_gene(self,gene)

    def add_todo(self, t, w=None, a=None, *args):
        '''添加todo,不会重复添加'''
        name = self.get_iter_name(t)
        for i in self.todo:
            if self.get_iter_name(i) == name:
                return
        self.todo.append((t, w, a, (t,)+args))  # 迭代器,执行完一步后的操作,迭代完后的操作,传递的参数

    def get_iter_name(self, iter):
        '''获取迭代器名称'''
        return str(iter).split()[2]

    def do_todo(self):
        i = 0
        while i < len(self.todo):
            try:
                next(self.todo[i][0])
                if self.todo[i][1]:
                    self.todo[i][1](*self.todo[i][3])
                i += 1
            except StopIteration:
                if self.todo[i][2]:
                    self.todo[i][2](*self.todo[i][3])
                self.todo.pop(i)
        for i in self.del_todo:
            try:
                self.todo.remove(i)
            except:
                pass

    def remove_todo(self, todo):
        '''删除todo'''
        self.del_todo.append(todo)
