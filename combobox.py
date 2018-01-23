# -*- coding: utf-8 -*-

import imp
try:
    imp.find_module('PySide2')
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *
except ImportError:
    from PySide.QtGui import *
    from PySide.QtCore import *


class HeaderComboBox(QWidget):
    """HeaderComboBox class
    ComboBox with header label. This is useful when you layout the pairs out label and comboBox.
    """

    #---------------------------------------------------------------------------
    ## SIGNALS
    activated = Signal(int)
    currentIndexChanged = Signal(int)
    editTextChanged = Signal(unicode)
    highlighted = Signal(int)


    #---------------------------------------------------------------------------
    ## コンストラクタ。ヘッダーとアイテムを指定できる。
    # @param header (str) : [= ""]
    # @param items (list) : [= []] list of strings
    # @param parent (QWidget) : [= None]
    # @return None
    def __init__(self, header = "", items = [], parent = None):
        super(HeaderComboBox, self).__init__(parent)
        self._header = header
        self._items = items
        self._prevIdx = 0
        self._initUI()
        self._setSignals()


    #---------------------------------------------------------------------------
    ## UI設定メソッド(隠蔽)
    # @return None
    def _initUI(self):
        self.mainLayout = QBoxLayout(QBoxLayout.TopToBottom)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        self.headerLabel = QLabel(self._header)
        self.mainLayout.addWidget(self.headerLabel)

        self.mainCombo = QComboBox()
        self.mainCombo.setEditable(True)
        self.mainCombo.addItems(self._items)
        self.mainCombo.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.mainCombo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.mainCombo.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.mainLayout.addWidget(self.mainCombo)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)


    #---------------------------------------------------------------------------
    ## シグナル設定メソッド(隠蔽)
    # @return None
    def _setSignals(self):
        self.mainCombo.activated.connect(self._activatedEvent)
        self.mainCombo.currentIndexChanged.connect(self.currentIndexChanged.emit)
        self.mainCombo.editTextChanged.connect(self.editTextChanged.emit)
        self.mainCombo.highlighted.connect(self.highlighted.emit)


    #---------------------------------------------------------------------------
    ## アイテムが選択もしくはテキストエディットが決定した際のスロット(隠蔽)
    # @param idx (int) : コンボボックスのアイテムインデックス
    # @return None
    def _activatedEvent(self, idx):
        text = self.mainCombo.itemText(idx)
        if text not in self._items:
            self.mainCombo.removeItem(idx)
            self.mainCombo.setCurrentIndex(self._prevIdx)
            self.activated.emit(self._prevIdx)

        else:
            self.mainCombo.setCurrentIndex(idx)
            self._prevIdx = idx
            self.activated.emit(idx)


    #---------------------------------------------------------------------------
    ## コンボボックスのアイテムを全部削除するメソッド
    # @return None
    def clearItems(self):
        self.mainCombo.clear()


    #---------------------------------------------------------------------------
    ## 現在コンボボックスで選択されているアイテムのインデックスを取得するメソッド
    # @return index (int) : インデックス
    def currentIndex(self):
        return self.mainCombo.currentIndex()


    #---------------------------------------------------------------------------
    ## 現在コンボボックスで選択されているアイテムのテキストを取得するメソッド
    # @return text (unicode) : テキスト
    def currentText(self):
        return self.mainCombo.currentText()


    #---------------------------------------------------------------------------
    ## 指定されたアイテムインデックスのデータを取得
    # @param idx (int) : コンボボックスのアイテムインデックス
    # @return data (object) : setItemDataでセットした値
    def itemData(self, idx):
        return self.mainCombo.itemData(idx)


    #---------------------------------------------------------------------------
    ## 指定されたアイテムインデックスのテキストを取得
    # @param idx (int) : コンボボックスのアイテムインデックス
    # @return itemText (unicode) : テキスト
    def itemText(self, idx):
        return self.mainCombo.itemText(idx)


    #---------------------------------------------------------------------------
    ## コンボボックスのLineEditを利用可能にするかどうかの設定。
    # @param editable (bool) : 設定
    # @return None
    def setComboEditable(self, editable):
        self.mainCombo.setEditable(editable)


    #---------------------------------------------------------------------------
    ## テキストを指定し、選択させる。アイテムにそのテキストが無い場合は何もしない。
    # @param text (str) : コンボボックスのアイテムテキスト
    # @return None
    def setCurrentText(self, text):
        idx = self.mainCombo.findText(text)
        if idx > -1:
            self.mainCombo.setCurrentIndex(idx)
        else:
            pass


    def setCurrentIndex(self, idx):
        self.mainCombo.setCurrentIndex(idx)


    #---------------------------------------------------------------------------
    ## ヘッダーを設定するメソッド
    # @param label (str) : ヘッダーテキスト
    # @return None
    def setHeader(self, label):
        self._header = label
        self.headerLabel.setText(self._header)


    #---------------------------------------------------------------------------
    ## ヘッダーの最小サイズを設定するメソッド
    # @param width (int) : ヘッダーの最小幅
    # @return None
    def setHeaderMinWidth(self, width):
        self.headerLabel.setMinimumWidth(width)


    #---------------------------------------------------------------------------
    ## カスタムデータをアイテムに設定するメソッド
    # @param idx (int) : アイテムインデックス
    # @param value (object) : カスタムデータバリュー
    # @return None
    def setItemData(self, idx, value):
        self.mainCombo.setItemData(idx, value)


    #---------------------------------------------------------------------------
    ## アイテムを設定するメソッド。
    # @param items (list) : 文字列のリスト
    # @return None
    def setItems(self, items):
        self._items = items
        self.mainCombo.blockSignals(True)
        self.mainCombo.clear()
        self.mainCombo.addItems(self._items)
        self.mainCombo.blockSignals(False)
        self.mainCombo.setCurrentIndex(0)
        self.mainCombo.currentIndexChanged.emit(0)


    #---------------------------------------------------------------------------
    ## アイテムの中に指定したテキストがあるかどうかを調べるメソッド。見つからない場合は-1が返る。
    # @param text (unicode) : 文字列
    # @param flags (Qt.MatchFlag)
    # @return int
    def findText(self, text, flags = Qt.MatchExactly | Qt.MatchCaseSensitive):
        return self.mainCombo.findText(text, flags)


    def direction(self):
        return self.mainLayout.direction()


    def setDirection(self, direction):
        self.mainLayout.setDirection(direction)
