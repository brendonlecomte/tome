from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, \
                            QTextBrowser, QListWidget, QTextEdit


class viewtab(QWidget):
    def __init__(self, parent, name, text):
        super().__init__()
        self.parent = parent
        self._initTab(name, text)

    def _initTab(self, name, text):
        self.setObjectName(name)
        self.layout = QVBoxLayout(self)
        self.dataTextView = QTextBrowser(self)
        self.layout.addWidget(self.dataTextView)
        self.dataTextView.insertHtml(text)


class searchTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self._initTab()

    def _initTab(self):
        self.setObjectName("Search")
        self.layout = QVBoxLayout(self)
        self.searchResult = QListWidget(self)
        self.searchBar = QTextEdit(self)
        self.searchBar.textChanged.connect(self._textChanged)
        self.searchResult.doubleClicked.connect(self._open)
        self.layout.addWidget(self.searchBar)
        self.layout.addWidget(self.searchResult)

    def _textChanged(self):
        text = self.searchBar.toPlainText()
        self.searchResult.clear()
        if text is not "":
            res = self.parent.controller.search(text)
            # print(res)
            for i in res:
                self.searchResult.addItem(i['object_type']+":"+i['name'])

    def _open(self):
        group, name = self.searchResult.currentItem().text().split(':')
        obj = self.parent.controller.getExact(group, name)
        text = self.parent.controller.convertToUI(obj)
        self.parent.openTab(name, text)

    def resizeEvent(self, event):
        pass  # size = self.parent.size()


class tabManager(QTabWidget):
    def __init__(self, controller):
        super().__init__()
        self.tabs = []
        self.controller = controller
        self.setTabsClosable(True)
        self.setObjectName("dataTabView")
        self.tabCloseRequested.connect(self.closeTab)

    def closeCurrent(self):
        self.closeTab(self.currentIndex())

    def closeTab(self, index):
        self.removeTab(index)

    def openTab(self, name, text):
        newTab = viewtab(self, name, text)
        self.addTab(newTab, name)
        self.setCurrentWidget(newTab)

    def openSearch(self):
        newTab = searchTab(self)
        self.addTab(newTab, "Search")
        self.setCurrentWidget(newTab)
