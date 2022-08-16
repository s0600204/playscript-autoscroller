
from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex


POSITION_ROLE = Qt.UserRole + 1
LEVEL_ROLE = Qt.UserRole + 2


class OutlineTreeNode:

    def __init__(self, parent=None):
        self._parent = parent
        self._children = []
        self._flags = Qt.ItemFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        self._text = None
        self._block_index = None
        self._header_level = 0

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    def addChild(self, child):
        self._children.append(child)

    def child(self, child_num):
        return self._children[child_num]

    def childCount(self):
        return len(self._children)

    def data(self, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._text

        if role == POSITION_ROLE:
            return self._block_index

        if role == LEVEL_ROLE:
            return self._header_level

        return None

    def index(self):
        return self.model().createIndex(self.rownum(), 0, self)

    def flags(self):
        return self._flags

    def model(self):
        return self._parent.model()

    def next_sibling(self):
        if self.rownum() < len(self._parent) - 1:
            return self._parent.children[self.rownum() + 1]
        return None

    def prev_sibling(self):
        if self.rownum():
            return self._parent.children[self.rownum() - 1]
        return None

    def removeChild(self, row):
        return self._children.pop(row)

    def rownum(self):
        if self._parent and self in self._parent.children:
            return self._parent.children.index(self)
        return -1

    def setData(self, value, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            self._text = value
            return True

        if role == POSITION_ROLE:
            self._block_index = value
            return True

        if role == LEVEL_ROLE:
            self._header_level = value
            return True

        return False

    def value(self):
        if self.rownum() > -1:
            return self.rownum()
        return self._parent.childCount()


class OutlineTreeRoot(OutlineTreeNode):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model = model

    def index(self):
        return QModelIndex()

    def model(self):
        return self._model


class OutlineTreeModel(QAbstractItemModel):

    def __init__(self):
        super().__init__()
        self._root = OutlineTreeRoot(self)

    def __len__(self):
        return self._root.childCount()

    def childCount(self, index):
        node = index.internalPointer() if index.isValid() else self._root
        return node.childCount()

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, self._root.childCount())
        while self._root.childCount() > 0:
            self._root.removeChild(0)
        self.endRemoveRows()

    def columnCount(self, index):
        # pylint: disable=no-self-use, unused-argument
        return 1

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        return index.internalPointer().data(role)

    def setData(self, index, value, role):
        # pylint: disable=no-self-use
        if not index.isValid():
            return False
        return index.internalPointer().setData(value, role)

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return index.internalPointer().flags()

    def index(self, row_num, col_num, parent_idx):
        if not self.hasIndex(row_num, col_num, parent_idx):
            return QModelIndex()

        parent_node = parent_idx.internalPointer() if parent_idx.isValid() else self._root
        child_node = parent_node.child(row_num)

        if child_node:
            return self.createIndex(row_num, col_num, child_node)
        return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        parent = index.internalPointer().parent
        if parent == self._root:
            return QModelIndex()

        return self.createIndex(parent.rownum(), 0, parent)

    def rowCount(self, index):
        return self.childCount(index)

    def determine_outline(self, document):
        self.clear()
        block = document.firstBlock()
        last_node = self._root
        while block.isValid():
            block_format = block.blockFormat()
            level = block_format.headingLevel()
            if level == 0:
                block = block.next()
                continue

            new_parent = last_node
            while new_parent.data(LEVEL_ROLE) >= level:
                new_parent = new_parent.parent

            new_node = OutlineTreeNode(parent=new_parent)
            new_node.setData(block.text(), Qt.DisplayRole)
            new_node.setData(block.position(), POSITION_ROLE)
            new_node.setData(level, LEVEL_ROLE)

            rownum = new_parent.childCount()

            self.beginInsertRows(new_parent.index(), rownum, rownum)
            new_parent.addChild(new_node)
            self.endInsertRows()

            last_node = new_node
            block = block.next()
