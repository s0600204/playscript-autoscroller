
from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex

try:
    from popplerqt5 import Poppler
except ModuleNotFoundError:
    Poppler = None

POSITION_ROLE = Qt.UserRole + 1
LEVEL_ROLE = Qt.UserRole + 2
PAGE_FRACTION = Qt.UserRole + 3


class OutlineTreeNode:

    def __init__(self, parent=None):
        self._parent = parent
        self._children = []
        self._flags = Qt.ItemFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        self._text = None
        self._block_index = None
        self._header_level = 0
        self._page_fraction = 0

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    def append_child(self, child):
        self._children.append(child)

    def child(self, child_num):
        return self._children[child_num]

    def child_count(self):
        return len(self._children)

    def data(self, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._text

        if role == POSITION_ROLE:
            return self._block_index

        if role == LEVEL_ROLE:
            return self._header_level

        if role == PAGE_FRACTION:
            return self._page_fraction

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

    def remove_child(self, row):
        return self._children.pop(row)

    def rownum(self):
        if self._parent and self in self._parent.children:
            return self._parent.children.index(self)
        return -1

    def set_data(self, value, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            self._text = value
            return True

        if role == POSITION_ROLE:
            self._block_index = value
            return True

        if role == LEVEL_ROLE:
            self._header_level = value
            return True

        if role == PAGE_FRACTION:
            self._page_fraction = value
            return True

        return False

    def value(self):
        if self.rownum() > -1:
            return self.rownum()
        return self._parent.child_count()


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
        return self._root.child_count()

    @property
    def has_content(self):
        return bool(len(self))

    def childCount(self, index):
        # pylint: disable=invalid-name
        node = index.internalPointer() if index.isValid() else self._root
        return node.child_count()

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, self._root.child_count())
        while self._root.child_count() > 0:
            self._root.remove_child(0)
        self.endRemoveRows()

    def columnCount(self, index):
        # pylint: disable=invalid-name, unused-argument
        return 1

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        return index.internalPointer().data(role)

    def setData(self, index, value, role):
        # pylint: disable=invalid-name
        if not index.isValid():
            return False
        return index.internalPointer().set_data(value, role)

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
        # pylint: disable=invalid-name
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
            new_node.set_data(block.text(), Qt.DisplayRole)
            new_node.set_data(block.position(), POSITION_ROLE)
            new_node.set_data(level, LEVEL_ROLE)

            rownum = new_parent.child_count()

            self.beginInsertRows(new_parent.index(), rownum, rownum)
            new_parent.append_child(new_node)
            self.endInsertRows()

            last_node = new_node
            block = block.next()

    def determine_from_pdf(self, pdf_document):
        self.clear()
        toc = pdf_document.toc()
        if not toc:
            return

        def walk_toc(toc_elem, model_parent):
            while not toc_elem.isNull():

                # Determine page number to scroll to when selecting this option
                toc_elem_attrs = toc_elem.attributes()
                if toc_elem_attrs.contains('Destination'):
                    destination = toc_elem_attrs.namedItem('Destination')
                    destination = Poppler.LinkDestination(destination.nodeValue())
                elif toc_elem_attrs.contains('DestinationName'):
                    destination = toc_elem_attrs.namedItem('DestinationName')
                    destination = pdf_document.linkDestination(destination.nodeValue())
                else:
                    destination = None

                new_node = OutlineTreeNode(parent=model_parent)
                new_node.set_data(toc_elem.nodeName(), Qt.DisplayRole)
                new_node.set_data(destination and destination.pageNumber() or 1, POSITION_ROLE)
                new_node.set_data(destination and destination.top() % 1 or 0, PAGE_FRACTION)
                # The `% 1` above is for when a target's `Destination` gives a value >= `1.0`.

                rownum = model_parent.child_count()
                self.beginInsertRows(model_parent.index(), rownum, rownum)
                model_parent.append_child(new_node)
                self.endInsertRows()

                if toc_elem.hasChildNodes():
                    walk_toc(toc_elem.firstChild(), new_node)

                toc_elem = toc_elem.nextSibling()

        walk_toc(toc.documentElement(), self._root)
