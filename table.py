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

import utility as util


class ConfigTableWidget(QTableWidget):
    """ConfigTableWidget class
    テーブルの各カラムの設定を辞書のリストで容易に設定できるテーブル。
    例）[{'key':'name', 'display':'Name', 'type':'str', 'visible':True, 'width':200}]
    typeはaddItemに与えるデータの各キーの値の型。'int','bool','str','list','dict'が指定可能。
    データは階層型辞書でも可（2階層まで）。その際はsubKey、subTypeを指定する。
    各セルデータの追加も、辞書データを渡すことで対応するキーの値を各カラムに追加できる。
    追加の処理が必要な場合はサブクラス化し、addItemメソッド等を上書きする。
    """

    KEY     = "key"
    SUBKEY  = "subKey"
    DISPLAY = "display"
    WIDTH   = "width"
    TYPE    = "type"
    SUBTYPE = "subType"
    VISIBLE = "visible"
    SEPARATOR = ", "


    #---------------------------------------------------------------------------
    ## コンストラクタ。テーブル設定データをここで渡す。
    # @param configuration (list) : list of dict. 詳細はクラスディスクリプションに記述
    # @param parent (QWidget) : [= None]
    # @return None
    def __init__(self, configuration, parent = None):
        super(ConfigTableWidget, self).__init__(parent)
        self._config = configuration
        self._parent = parent
        self._initSettings()
        self.setSignals()
        self._setHeaderSetting()


    #-------------------------------------------------------------------------
    ## apply initial settings for table view parameters
    # @param None
    # @return None
    def _initSettings(self):
        self.setColumnCount(len(self._config))
        self.setHorizontalHeaderLabels(util.makeListByDictKey(self.DISPLAY, self._config))
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(20)
        self.horizontalHeader().setMovable(True)
        self.horizontalHeader().setResizeMode(QHeaderView.Interactive)
        self.setSortingEnabled(True)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)


    #-------------------------------------------------------------------------
    ## set signals
    # @param None
    # @return None
    def setSignals(self):
        pass


    #-------------------------------------------------------------------------
    ## set headers
    # @param None
    # @return None
    def _setHeaderSetting(self):

        for i, colInfo in enumerate(self._config):
            self.setColumnVisibe(i, colInfo.get(self.VISIBLE))
            if colInfo.get(self.WIDTH) is not None:
                self.setColumnWidth(i, colInfo.get(self.WIDTH))


    #-------------------------------------------------------------------------
    ## 設定情報のキーを渡して、カラム番号を返すメソッド。カラムの辞書データをそのまま渡すか、キーを指定する。
    # サブキーがある場合はサブキーを指定する。
    # @param colInfo (dict) : 設定情報の各カラムの辞書
    # @param key (str) : カラムのキー
    # @param subKey (str) : カラムのサブキー
    # @return section (int) : カラム番号
    def getHeaderSectionByKey(self, colInfo = None, key = None, subKey = None):
        if key is None and subKey is None and colInfo is None:
            raise ValueError("The arguments, 'colInfo' or 'key', must be supecified.")

        if colInfo is not None:
            key = colInfo.get(self.KEY)
            subKey = colInfo.get(self.SUBKEY)

        for i, item in enumerate(self._config):
            if item.get(self.KEY) == key:
                if item.has_key(self.SUBKEY):
                    if item.get(self.SUBKEY) == subKey:
                        return i
                    else:
                        continue
                else:
                    return i
            else:
                continue

        raise AttributeError("Configuration doesn't have specified key or information.")


    #-------------------------------------------------------------------------
    ## カラムのShow/Hide切り替えメソッド。
    # @param col (int) : カラム番号
    # @param visible (bool) : Trueで表示、Falseで非表示にする。
    # @return None
    def setColumnVisibe(self, col, visible):
        if visible:
            self.showColumn(col)
        else:
            self.hideColumn(col)


    #-------------------------------------------------------------------------
    ## 値を表示用に変換するメソッド
    # @param value (object) : 値
    # @param colType (str) : valueのタイプ。(str,string,int,bool)
    # @return converted (string) : 変換できない場合、空文字列が返る。
    def _makeItemString(self, value, colType):
        if value is None:
            return ""
        if colType in ("str", "string"):
            return value
        if colType in ("int"):
            return str(value)
        if colType in ("bool"):
            return str(value)

        return ""


    #-------------------------------------------------------------------------
    ## 新しくテーブルにアイテムを追加するメソッド。辞書を引数に取り、キーが対応するカラムに値を入れていく。
    # カラムのデータが取れない場合は空文字列のアイテムが作成される。
    # オリジナルの辞書データも作成されたアイテムのitemData属性にセットされる。同じ行のアイテム同士は同じ辞書データを参照しあう。
    # @param itemData (dict) : 各カラムの値を持った辞書
    # @return addedItems (list) : QTableWidgetItemのリスト
    def addItem(self, itemData):

        currentRowCount = self.rowCount()
        self.setRowCount(currentRowCount+1)

        row = currentRowCount
        addedItems = []
        for col, colInfo in enumerate(self._config):

            try:
                label = self._setItemCore(colInfo, itemData)
            except AttributeError:
                label = ""

            item = QTableWidgetItem(label)
            item.itemData = itemData
            self.setItem(row, col, item)
            addedItems.append(item)

        return addedItems


    #-------------------------------------------------------------------------
    ## アイテムデータを更新するメソッド。変更するカラムのキーと値の入った辞書を渡す。
    # 対応するキーが見つからない場合は何もしない。
    # また同時にQTableWidgetItemが持っているオリジナルデータも更新するので、QTableWidgetItemを直接
    # 更新するのではなく、このメソッドを介して更新するほうがよい。
    # @param itemData (dict) : 各カラムの値を持った辞書
    # @return addedItems (list) : QTableWidgetItemのリスト
    def updateItemAt(self, row, itemData):
        updated = []
        for col, colInfo in enumerate(self._config):
            try:
                label = self._setItemCore(colInfo, itemData)
            except AttributeError:
                continue
            targetItem = self.item(row, col)
            targetItem.setText(label)
            targetItem.itemData.update(itemData)
            updated.append(targetItem)

        return updated


    #-------------------------------------------------------------------------
    ## カラムの設定情報を用いて、itemDataから必要なデータを取り出し、型に合わせて文字列を作成する。
    # @param colInfo (dict) : テキスト化したいカラムの情報
    # @param itemData (dict) : 各カラムの値を持った辞書
    # @return label (str) : カラムの文字列
    def _setItemCore(self, colInfo, itemData):
        hKey = colInfo[self.KEY]
        hType = colInfo[self.TYPE]

        if not itemData.has_key(hKey):
            raise AttributeError("Data doesn't have key '%s'." % hKey)

        value = itemData.get(hKey, "")

        if hType == "dict":
            hSubKey = colInfo.get(self.SUBKEY)
            hSubType = colInfo.get(self.SUBTYPE)

            if not value.has_key(hSubKey):
                raise AttributeError("Data doesn't have subKey '%s' of key '%s'." % (hSubKey, hKey))

            subValue = value.get(hSubKey)
            label = self._makeItemString(subValue, hSubType)

        elif hType == "list" and isinstance(value, list):
            hSubType = colInfo.get(self.SUBTYPE)

            if hSubType == "dict":
                hSubKey = colInfo.get(self.SUBKEY)
                labels = util.makeListByDictKey(hSubKey, value)
                label = self.SEPARATOR.join(labels)

            else:
                label =self.SEPARATOR.join([self._makeItemString(v, hSubType) for v in value])

        else:
            label = self._makeItemString(value, hType)

        return label


    #-------------------------------------------------------------------------
    ## テーブルのアイテムを空にするとともに、行数もリセットする。
    # @param None
    # @return None
    def clearAll(self):
        self.clearContents()
        self.setRowCount(0)


    #-------------------------------------------------------------------------
    ## 現在選択されている行のリストを返す。重複なし。
    # @return rows (list) : 行番号のリスト。ソートされている。
    def selectedRows(self):
        sels = self.selectedItems()
        rows = set()
        for selItem in sels:
            rows.add(selItem.row())

        return sorted(list(rows))


    #-------------------------------------------------------------------------
    ## 指定されたカラムのデータリストを作成して返すメソッド。直接カラム番号を指定するか、key、subKeyで指定する。
    # どちらも指定されなかった場合はValueErrorが返る。型変換が必要な場合はvalTypeを指定する。
    # @param col (int) : カラムインデックス [= None]
    # @param key (str) : カラム設定のキー [= None]
    # @param subKey (str) : カラム設定のサブキー [= None]
    # @param valType (str) : データの型指定 [= None]
    # @return list (list) : カラムのデータリスト
    def getSelectItemsAt(self, col = None,  key = None, subKey = None, valType = None):
        if isinstance(col, int):
            keyCol = col

        elif col is None and isinstance(key, (str, unicode)):
                keyCol = self.getHeaderSectionByKey(key = key, subKey = subKey)

        else:
            raise ValueError

        resList = set()
        sels = self.selectedItems()
        for selItem in sels:
            itemRow = selItem.row()
            keyItem = self.item(itemRow, keyCol)
            if valType == "int":
                value = int(keyItem.text())
            elif valType in ("str" or "string"):
                value = str(keyItem.text())
            else:
                value = keyItem.text()

            resList.add(value)

        return list(resList)


    #-------------------------------------------------------------------------
    ## カラムのソートをキーによって行う。昇順、降順の指定も可能
    # @param key (str) : カラム設定のキー
    # @param subKey (str) : カラム設定のサブキー [= None]
    # @param order (Qt.SortOrder) : ソートタイプ [= Qt.AscendingOrder]
    # @return None
    def sortItemsByKey(self, key, subKey = None, order = Qt.AscendingOrder):
        keyCol = self.getHeaderSectionByKey(key = key, subKey = subKey)
        self.sortItems(keyCol, order)


    #-------------------------------------------------------------------------
    ## ある行におけるデータを全て取得するメソッド。
    # @param row (int) : 行インデックス
    # @return itemData (dict) : 行を作る際に用いた辞書データ
    def getItemDataAt(self, row):
        item = self.item(row, 0)
        try:
            return item.itemData
        except Exception as err:
            raise err


    #-------------------------------------------------------------------------
    ## 列アイテムの中で指定した値を持つアイテムを取得する。見つからなかった場合はNoneが返る。
    # @param col (int) : 列インデックス
    # @param value (str or unicode)
    # @return item (QTableWidgetItem)
    def getItemByValue(self, col, value):
        for row in range(self.rowCount()):
            item = self.item(row, col)
            if item is None:
                continue
            if item.text() == value:
                return item
        return None


