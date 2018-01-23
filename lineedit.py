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

import completer as cpl


class HeaderLineEdit(QWidget):


    def __init__(self, header = "", placeholder = "", direction = QBoxLayout.LeftToRight, parent = None):
        super(HeaderLineEdit, self).__init__(parent)
        self._initUI(header, placeholder)
        self.setDirection(direction)


    def _initUI(self, header, placeholder):
        self.mainLayout = QBoxLayout(QBoxLayout.LeftToRight)
        self.setLayout(self.mainLayout)

        self.headerLabel = QLabel(header)
        self.mainLayout.addWidget(self.headerLabel)

        self.lineEdit = QLineEdit(placeholder)
        self.mainLayout.addWidget(self.lineEdit)


    #---------------------------------------------------------------------------
    ## ボタン配置の方向を設定するメソッド
    # @param direction (QBoxLayout.Direction) : 配置方向
    # @return None
    def setDirection(self, direction):
        self.mainLayout.setDirection(direction)


    def setHeaderMinimumWidth(self, width):
        self.headerLabel.setMinimumWidth(width)


    def setHeaderMinimumHeight(self, height):
        self.headerLabel.setMinimumHeight(height)


    def setHeaderMinimumSize(self, *args):
        self.headerLabel.setMinimumSize(*args)


    def setHeaderMaximumWidth(self, width):
        self.headerLabel.setMaximumWidth(width)


    def setHeaderMaximumHeight(self, height):
        self.headerLabel.setMaximumHeight(height)


    def setHeaderMaximumSize(self, *args):
        self.headerLabel.setMaximumSize(*args)


    def clear(self):
        self.lineEdit.clear()


    def completer(self):
        return self.lineEdit.completer()


    def cursorPosition(self):
        return self.lineEdit.cursorPosition()


    def hasAcceptableInput(self):
        return self.lineEdit.hasAcceptableInput()


    def inputMask(self):
        return self.lineEdit.inputMask()


    def placeholderText(self):
        return self.lineEdit.placeholderText()


    def selectAll(self):
        return self.lineEdit.selectAll()


    def selectedText(self):
        return self.lineEdit.selectedText()


    def setCompleter(self, completer):
        self.lineEdit.setCompleter(completer)


    def setHeader(self, header):
        self.headerLabel.setText(header)


    def getHeader(self):
        return self.headerLabel.text()


    def setInputMask(self, inputMask):
        self.lineEdit.setInputMask(inputMask)


    def setPlaceholderText(self, placeholder):
        self.lineEdit.setPlaceholderText(placeholder)


    def setReadOnly(self, only):
        self.lineEdit.setReadOnly(only)


    def setText(self, text):
        self.lineEdit.setText(text)


    def text(self):
        return self.lineEdit.text()



class MultiCompleteEdit(QLineEdit):
    """MultiCompleteEdit class
    通常のCompleterはLineEdit内の文字列全体を対象に補完が行われるが
    文字列の補完をLineEdit内の単語単位で行うことができるウィジェット
    """

    completed = Signal(str)


    #---------------------------------------------------------------------------
    ## コンストラクタ。
    # @param model (list) : [= []] list of strings
    # @param separator (string) : [= ","] default is comma
    # @param addSpaceAfterCompleting (bool) : [= True] 補完後の文字列の最後にスペースを入れるかどうか
    # @param parent (QWidget) : [= None]
    # @return None
    def __init__(self, model = [], separator = ',', addSpaceAfterCompleting = True, parent = None):
        super(MultiCompleteEdit, self).__init__(parent)
        self._caseSensitivity = Qt.CaseInsensitive
        self._separator = separator
        self._addSpaceAfterCompleting = addSpaceAfterCompleting
        self._completer = QCompleter(model)
        self._completer.setWidget(self)
        self._completer.setCaseSensitivity(self._caseSensitivity)
        self.connect(self._completer, SIGNAL('activated(QString)'), self._insertCompletion)
        self._keysToIgnore = [Qt.Key_Enter,
                              Qt.Key_Return,
                              Qt.Key_Escape,
                              Qt.Key_Tab]


    #---------------------------------------------------------------------------
    ## コンプリータの補完ポップアップからアイテムが選択されたときに呼ばれる。現在入力が完了している文字列に
    # 不足分を追加して、LineEditの文字列にする。
    # @param completion (str) : 補完文字列
    # @return None
    def _insertCompletion(self, completion):
#         extra = len(completion) - len(self._completer.completionPrefix())
#
#         if extra == 0:
#             extra_text = ""
#         else:
#             extra_text = completion[-extra:]
        lastLabel = self.text()[:-len(self._completer.completionPrefix())]

        if self._addSpaceAfterCompleting:
            fcompletion = completion + self._separator+' '
        else:
            fcompletion = completion

        self.setText(lastLabel + fcompletion)
        self.completed.emit(completion)



    #---------------------------------------------------------------------------
    ## 現在のカーソル位置から、セパレータまでの文字列を一単語として返すメソッド。
    # @return textUnderCursor (str) : 空文字、セパレータ無しの文字列
    def textUnderCursor(self):
        text = self.text()
        textUnderCursor = ''
        i = self.cursorPosition() - 1

        while i >=0 and text[i] != self._separator:
            textUnderCursor = text[i] + textUnderCursor
            i -= 1

        if self._addSpaceAfterCompleting and\
           len(textUnderCursor) > 0 and\
           textUnderCursor[0] == " ":
            textUnderCursor = textUnderCursor[1:]

        return textUnderCursor


    #---------------------------------------------------------------------------
    ## keyPressEventのオーバーライド。一番後ろの単語のみを補完対象にする。また、補完ポップアップが出てる
    # 状態で打ち続けて、補完が必要なくなったときにポップアップを消す。
    # @param event (QKeyEvent) : イベントオブジェクト
    # @return None
    def keyPressEvent(self, event):
        if self._completer.popup().isVisible():
            if event.key() in self._keysToIgnore:
                event.ignore()
                return
        super(MultiCompleteEdit, self).keyPressEvent(event)
        completionPrefix = self.textUnderCursor()

        if completionPrefix != self._completer.completionPrefix():
            self._updateCompleterPopupItems(completionPrefix)

        if len(event.text()) > 0 and len(completionPrefix) > 0:
            self.blockSignals(True) ## block emitting 'editingFinished' signal
            self._completer.complete()
            self.blockSignals(False)

        if len(completionPrefix) == 0:
            self._completer.popup().hide()



    #---------------------------------------------------------------------------
    ## 補完対象の文字列を強制的にセットするメソッド。
    # @param completionPrefix (str) : 補完文字
    # @return None
    def _updateCompleterPopupItems(self, completionPrefix):
        self._completer.setCompletionPrefix(completionPrefix)
        self._completer.popup().setCurrentIndex(
                self._completer.completionModel().index(0,0))


    #---------------------------------------------------------------------------
    ## 補完用の文字列リストをセットする関数。
    # @param items (list) : list of strings
    # @return None
    def setCompleteItems(self, items):
        self._completer = QCompleter(items)
        self._completer.setWidget(self)
        self._completer.setCaseSensitivity(self._caseSensitivity)
        self.connect(self._completer, SIGNAL('activated(QString)'), self._insertCompletion)


    #---------------------------------------------------------------------------
    ## 補完の強度を設定するメソッド。
    # @param caseSensitivity (Qt.CaseSensitivity)
    # @return None
    def setCaseSensitivity(self, caseSensitivity):
        self._caseSensitivity = caseSensitivity
        self._completer.setCaseSensitivity(self._caseSensitivity)


    #---------------------------------------------------------------------------
    ## 入力された文字列を切り出してリストとして取得するための関数。
    # @return words (list) : 入力された単語リスト
    def getTextList(self):
        text = self.text()
        if len(text) == 0:
            return []

        while text[-1] in [",", " "]:
            text = text[:-1]

        words = text.replace(", ", ",").split(",")
        #words = list(set(words))
        return words


class AnyPosMultiCompleteEdit(MultiCompleteEdit):


    def __init__(self, model = [], separator = ',', addSpaceAfterCompleting = True, parent = None):
        super(AnyPosMultiCompleteEdit, self).__init__(model, separator, addSpaceAfterCompleting, parent)
        self.setCompleteItems(model)


    def setCompleteItems(self, items):
        self._completer = cpl.AnyPosCompleter(items)
        self._completer.setWidget(self)
        self._completer.setCaseSensitivity(self._caseSensitivity)
        self.connect(self._completer, SIGNAL('activated(QString)'), self._insertCompletion)

