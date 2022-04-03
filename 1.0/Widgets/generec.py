from Widgets.basewidget import *


class GeneRec(BaseWidget):
    '''基因记录'''

    def __init__(self) -> None:
        super().__init__()
        self.resize(1000, 618)
        self.setWindowTitle('基因记录')

        self.genes = QListWidget(self)
        self.genes.__dict__['keyPressEvent'] = self.keyPressEvent
        self.genes.move(0, 0)

        self.record_genes = []  # 已经记录过的gene

    def resizeEvent(self, a0) -> None:
        self.genes.resize(self.width(), self.height())

    def add_gene(self, gene):
        '''添加基因'''
        _gene = '-'.join(map(str, gene))
        if _gene not in self.record_genes:
            self.genes.addItem('-'.join(map(str, gene)))
            self.record_genes.append(_gene)
            self.genes.setCurrentRow(self.genes.count()-1)
