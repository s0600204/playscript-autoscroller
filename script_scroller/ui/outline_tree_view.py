
from PyQt5.QtWidgets import (
    QTreeView,
)


class OutlineTreeView(QTreeView):

    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setModel(model)

        self.setItemsExpandable(False)
        self.setHeaderHidden(True)
        self.expandAll()
