# -*- coding: utf-8 -*-
import sys

import imp
try:
    imp.find_module('PySide2')
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *
except ImportError:
    from PySide.QtGui import *
    from PySide.QtCore import *

from functools import partial


class CenterCheckBox(QWidget):
    """CenterCheckBox class
    親Widgetやセルの真ん中にチェックボックスを配置するためのウィジェット。QListWidget、QTableWidgetなどで
    setItemWidgetしたものはalighnが効かなくなるため、そのような場合に使用する。
    """

    #---------------------------------------------------------------------------
    ## SIGNALS
    stateChanged = Signal(Qt.CheckState)
    clicked = Signal()
    pressed = Signal()
    released = Signal()


    #---------------------------------------------------------------------------
    ## コンストラクタ。
    # @param parent (QWidget) : [= None]
    # @return None
    def __init__(self, parent = None):
        super(CenterCheckBox, self).__init__(parent)
        self._parent = parent
        self._initUI()
        self._setSignals()


    #---------------------------------------------------------------------------
    ## UI設定メソッド(隠蔽)
    # @return None
    def _initUI(self):
        layout = QHBoxLayout()
        self.checkItem = QCheckBox(self)
        self.checkItem.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.checkItem.setCheckState(Qt.Checked)
        self.checkItem.setStyleSheet("background-color: transparent; border: none;")

        layout.addWidget(self.checkItem)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self.setLayout(layout)


    #---------------------------------------------------------------------------
    ## シグナル設定メソッド(隠蔽)
    # @return None
    def _setSignals(self):
        self.checkItem.stateChanged.connect(self._stateChangeEvent)
        self.checkItem.clicked.connect(self.clicked.emit)
        self.checkItem.pressed.connect(self.pressed.emit)
        self.checkItem.released.connect(self.released.emit)


    #---------------------------------------------------------------------------
    ## stateChangeシグナルをemitするためのフックメソッド(隠蔽)
    # @return None
    def _stateChangeEvent(self, state):
        if state == Qt.Unchecked:
            self.stateChanged.emit(Qt.Unchecked)
        elif state == Qt.Checked:
            self.stateChanged.emit(Qt.Checked)
        else:
            self.stateChanged.emit(Qt.PartiallyChecked)


    #---------------------------------------------------------------------------
    ## checkStateを返すメソッド。
    # @return None
    def checkState(self):
        return self.checkItem.checkState()


    #---------------------------------------------------------------------------
    ## checkStateをセットする。
    # @param state (Qt.CheckState)
    # @return None
    def setCheckState(self, state):
        self.checkItem.setCheckState(state)


    #---------------------------------------------------------------------------
    ## check可能かどうかの設定
    # @param checkable (bool)
    # @return None
    def setCheckable(self, checkable):
        self.checkItem.setCheckable(checkable)


    #---------------------------------------------------------------------------
    ## check可能かどうかを返す。
    # @return checkable (bool)
    def isCheckable(self):
        return self.checkItem.isCheckable()


    #---------------------------------------------------------------------------
    ## checkする
    # @param checked (bool)
    # @return None
    def setChecked(self, checked):
        self.checkItem.setChecked(checked)


    #---------------------------------------------------------------------------
    ## checkされているかどうかを返す
    # @return checked (bool)
    def isChecked(self):
        return self.checkItem.isChecked()


    #---------------------------------------------------------------------------
    ## ボタンが押されている状態にする。
    # param down (bool)
    # @return None
    def setDown(self, down):
        self.checkItem.setDown(down)


    #---------------------------------------------------------------------------
    ## ボタンが押されているかどうかを返す
    # @return down (bool)
    def isDown(self):
        return self.checkItem.isDown()



class CheckButtonGroup(QGroupBox):
    """CheckButtonGroup class
    ボタングループを簡単に作るためのクラス。ボタンの種類はチェックボックスとラジオボックスに対応。
    ボタンの並べ方も横並び、縦並びの設定ができる。
    """

    #---------------------------------------------------------------------------
    ## Class constants
    kCheckBoxType = 0
    kRadioBoxType = 1

    #---------------------------------------------------------------------------
    ## SIGNALS
    itemToggled = Signal(str, bool)
    itemClicked = Signal(str, bool)


    #---------------------------------------------------------------------------
    ## コンストラクタ。ボタンの対応や配置を設定できる。
    # @param title (str) : グループボックスのタイトル
    # @param description (str) : [= ""] グループボックスの説明文。省略可。
    # @param items (list) : [= []] list of strings
    # @param direction (QBoxLayout.Direction) : [= QBoxLayout.TopToBottom] ボタンの配置方向
    # @param buttonType (int) : [= kCheckBoxType] (kCheckBoxType or kRadioBoxType)
    # @param parent (QWidget) : [= None]
    # @return None
    def __init__(self, title, description = "", items = [], direction = QBoxLayout.TopToBottom, buttonType = kCheckBoxType, parent = None):
        super(CheckButtonGroup, self).__init__(title, parent)
        self._buttonType = buttonType
        self._initUI()
        self.setDirection(direction)
        self.setDescription(description)
        for item in items:
            self.addItem(item)


    #---------------------------------------------------------------------------
    ## UI設定メソッド(隠蔽)
    # @return None
    def _initUI(self):
        wrapLayout = QVBoxLayout()
        self.setLayout(wrapLayout)
        self._descriptionLabel = QLabel()
        wrapLayout.addWidget(self._descriptionLabel)
        self._descriptionLabel.hide()
        self.mainLayout = QBoxLayout(QBoxLayout.TopToBottom)
        wrapLayout.addLayout(self.mainLayout)


    #---------------------------------------------------------------------------
    ## ボタンアイテムを追加するメソッド。
    # @param name (str) : ボタンのラベル
    # @return None
    def addItem(self, name):
        if self._buttonType == self.kCheckBoxType:
            checkItem = QCheckBox(name)
        else:
            checkItem = QRadioButton(name)
        self.mainLayout.addWidget(checkItem)
        checkItem.toggled.connect(partial(self.itemToggleEvent, checkItem))
        checkItem.clicked.connect(partial(self.itemClickEvent, checkItem))


    #---------------------------------------------------------------------------
    ## ボタン配置の方向を設定するメソッド
    # @param direction (QBoxLayout.Direction) : 配置方向
    # @return None
    def setDirection(self, direction):
        self.mainLayout.setDirection(direction)


    #---------------------------------------------------------------------------
    ## グループボックスの説明をセットする。
    # @param description (str) : 説明文字列
    # @return None
    def setDescription(self, description):
        self._descriptionLabel.setText(description)


    def showDescription(self):
        self._descriptionLabel.show()


    def hideDescription(self):
        self._descriptionLabel.hide()


    def setDescriptionVisible(self, visible):
        self._descriptionLabel.setVisible(visible)


    def isDescriptionVisible(self):
        return self._descriptionLabel.isVisible()


    #---------------------------------------------------------------------------
    ## 指定された文字列すべてに一致するボタンのチェック状態をセットする。
    # @param names (list) : list of strings
    # @param check (bool) : [= True] チェック状態
    # @return None
    def setCheckedByNames(self, names, check = True):
        for i in range(self.mainLayout.count()):
            item = self.mainLayout.itemAt(i)
            buttonItem = item.widget()
            if not isinstance(buttonItem, (QCheckBox, QRadioButton)):
                continue

            label = buttonItem.text()
            if label in names:
                buttonItem.setChecked(check)
            else:
                buttonItem.setChecked(not check)


    #---------------------------------------------------------------------------
    ## 指定された文字列に一致するボタンのチェック状態をセットする。
    # @param name (str) : ボタンラベル
    # @param check (bool) : [= True] チェック状態
    # @return None
    def setCheckedByName(self, name, check = True):
        for i in range(self.mainLayout.count()):
            item = self.mainLayout.itemAt(i)
            buttonItem = item.widget()
            if not isinstance(buttonItem, (QCheckBox, QRadioButton)):
                continue

            label = buttonItem.text()
            if label == name:
                buttonItem.setChecked(check)
            else:
                buttonItem.setChecked(not check)


    #---------------------------------------------------------------------------
    ## 指定されたインデックスにおけるボタンのチェック状態を設定する。
    # @param idx (int) : ボタンのインデックス番号
    # @param check (bool) : [= True] チェック状態
    # @param exclusive (bool) : [= True] 排他的処理をするか
    # @return None
    def setCheckedByIndex(self, idx, check = True, exclusive = True):

        if idx >= self.mainLayout.count():
            raise IndexError("Specified index is more than item count.")

        item = self.mainLayout.itemAt(idx)
        buttonItem = item.widget()

        if not isinstance(buttonItem, (QCheckBox, QRadioButton)):
            raise ValueError("Specified item is not checkable.")

        if exclusive:
            if check:
                self.uncheckAll()
            else:
                self.checkAll()

        buttonItem.setChecked(check)


    #---------------------------------------------------------------------------
    ## ボタンにアイコンをセットするメソッド。
    # @param idx (int) : ボタンのインデックス番号
    # @param icon (QIcon) : アイコンオブジェクト
    # @return None
    def setIcon(self, idx, icon):
        if idx >= self.mainLayout.count():
            raise IndexError("Specified index is more than item count.")

        item = self.mainLayout.itemAt(idx)
        buttonItem = item.widget()
        buttonItem.setIcon(icon)


    #---------------------------------------------------------------------------
    ## チェックされてるボタンのテキストのリストを取得する。
    # @return checkedNames (list) : list of strings
    def getCheckedNames(self):
        checkNames = []
        for i in range(self.mainLayout.count()):
            item = self.mainLayout.itemAt(i)
            buttonItem = item.widget()
            if not isinstance(buttonItem, (QCheckBox, QRadioButton)):
                continue

            if buttonItem.isChecked():
                label = buttonItem.text()
                checkNames.append(label)

        return checkNames


    #---------------------------------------------------------------------------
    ## チェックされてるボタンのインデックスのリストを取得する。
    # @return checks (list) : list of int
    def getCheckedIndices(self):
        checks = []
        for i in range(self.mainLayout.count()):
            item = self.mainLayout.itemAt(i)
            buttonItem = item.widget()
            if not isinstance(buttonItem, (QCheckBox, QRadioButton)):
                continue

            if buttonItem.isChecked():
                checks.append(i)
        return checks


    #---------------------------------------------------------------------------
    ## ボタンのトグルをemitするメソッド
    # @param item (QAbstractButton) : トグルが発生したアイテム
    # @param checked (bool)
    # @return None
    def itemToggleEvent(self, item, checked):
        name = item.text()
        self.itemToggled.emit(name, checked)


    def itemClickEvent(self, item):
        name = item.text()
        checked = item.isChecked()
        self.itemClicked.emit(name, checked)


    #---------------------------------------------------------------------------
    ## ボタンのテキスト名からボタンアイテムのインデックス番号を取得するメソッド。一致するものがない場合は-1が返る。
    # @param name (str) : ボタン名
    # @return idx (int)
    def indexOf(self, name):
        for i in range(self.mainLayout.count()):
            item = self.mainLayout.itemAt(i)
            buttonItem = item.widget()
            if not isinstance(buttonItem, (QCheckBox, QRadioButton)):
                continue

            if buttonItem.text() == name:
                return i

        return -1

    #---------------------------------------------------------------------------
    ## ボタンアイテムのインデックス番号からボタン名を取得
    # @param idx (int)
    # @return name (str) : ボタン名
    def nameAt(self, idx):
        if idx >= self.mainLayout.count():
            raise IndexError("Specified index is more than item count.")

        item = self.mainLayout.itemAt(idx)
        buttonItem = item.widget()
        if not isinstance(buttonItem, (QCheckBox, QRadioButton)):
            raise ValueError("The item at the index is not button.")

        return buttonItem.text()


    #---------------------------------------------------------------------------
    ## 全てのボタンにチェックを入れる
    # @return None
    def checkAll(self):
        self._checkAll(True)


    #---------------------------------------------------------------------------
    ## 全てのボタンのチェックを外す
    # @return None
    def uncheckAll(self):
        self._checkAll(False)


    #---------------------------------------------------------------------------
    ## 全てのボタンのチェックを設定する。（隠蔽）
    # @param check (bool)
    # @return None
    def _checkAll(self, check):

        for i in range(self.mainLayout.count()):
            item = self.mainLayout.itemAt(i)
            buttonItem = item.widget()
            if not isinstance(buttonItem, (QCheckBox, QRadioButton)):
                continue

            if self._buttonType == self.kRadioBoxType:
                buttonItem.setAutoExclusive(False)

            buttonItem.setChecked(check)

            if self._buttonType == self.kRadioBoxType:
                buttonItem.setAutoExclusive(True)





