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

from functools import partial

from CustomWidgets import combobox
from CustomWidgets import button
from CustomWidgets import lineedit


class exampleGUI(QMainWindow):

    def __init__(self):
        super(exampleGUI, self).__init__()
        self.setWindowTitle("Example Window")
        self._initUI()


    def _initUI(self):
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        wrapWidget = QWidget(self)
        self.setCentralWidget(wrapWidget)
        wrapWidget.setLayout(mainLayout)

        headerComboHeader = QLabel("---- HeaderCombo ----")
        mainLayout.addWidget(headerComboHeader)
        headerComboArea = QHBoxLayout()
        mainLayout.addLayout(headerComboArea)
        v_hcombo = combobox.HeaderComboBox("Blood Type", ["A", "B", "O", "AB"], self)
        headerComboArea.addWidget(v_hcombo)
        h_hcombo = combobox.HeaderComboBox("Name", ["Taro", "Hanako", "Jiro", "Sakura"], self)
        h_hcombo.setDirection(QBoxLayout.LeftToRight)
        h_hcombo.setHeaderMinWidth(100)
        headerComboArea.addWidget(h_hcombo)
        
        centerCheckBoxHeader = QLabel("---- CenterCheckBox ----")
        centerCheckBoxDesc = QLabel("This widget is useful for table or list widget item cell\nbecause usually check box appears left or right aligned position.")
        mainLayout.addWidget(centerCheckBoxHeader)
        mainLayout.addWidget(centerCheckBoxDesc)
        centerCheckBoxWrap = QLabel("")
        centerCheckBoxWrap.setMinimumWidth(100)
        centerCheckBoxWrap.setMinimumHeight(40)
        centerCheckBoxWrap.setStyleSheet("border: 1px solid #3A3939;")
        ch = QVBoxLayout()
        centerCheckBoxWrap.setLayout(ch)
        centerCheckBox = button.CenterCheckBox(self)
        ch.addWidget(centerCheckBox)
        mainLayout.addWidget(centerCheckBoxWrap)

        checkBtnGPHeader = QLabel("---- CheckButtonGroup (CheckBox) ----")
        mainLayout.addWidget(checkBtnGPHeader)
        self.checkBtnGroup = button.CheckButtonGroup("Favourite Foods",
                                                     "This is sample of checkBox type",
                                                     ["Sushi", "Curry", "Ramen"],
                                                     parent = self)
        mainLayout.addWidget(self.checkBtnGroup)
        checkSettingArea = QHBoxLayout()
        mainLayout.addLayout(checkSettingArea)

        chVDirectionBtn = QPushButton("Vertical")
        chVDirectionBtn.clicked.connect(partial(self.changeCheckButtonDirection, "v"))
        checkSettingArea.addWidget(chVDirectionBtn)

        chHDirectionBtn = QPushButton("Horizontal")
        chHDirectionBtn.clicked.connect(partial(self.changeCheckButtonDirection, "h"))
        checkSettingArea.addWidget(chHDirectionBtn)

        chShowDescBtn = QPushButton("Toggle Description")
        chShowDescBtn.clicked.connect(self.checkBtnGrpToggleEvent)
        checkSettingArea.addWidget(chShowDescBtn)

        radioBtnGPHeader = QLabel("---- CheckButtonGroup (RadioBox) ----")
        mainLayout.addWidget(radioBtnGPHeader)
        self.radioBtnGroup = button.CheckButtonGroup("Gender",
                                                     "This is sample of radioBox type",
                                                     ["Male", "Female"],
                                                     buttonType=button.CheckButtonGroup.kRadioBoxType,
                                                     parent = self)
        mainLayout.addWidget(self.radioBtnGroup)
        self.radioBtnGroup.setCheckedByName("Male")

        multiCompHeader = QLabel("---- MultiCompleteEdit ----")
        mainLayout.addWidget(multiCompHeader)
        multiCompDesc = QLabel("Type day of week")
        mainLayout.addWidget(multiCompDesc)
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        multiLine = lineedit.MultiCompleteEdit(days, parent = self)
        mainLayout.addWidget(multiLine)

        anyposMultiCompHeader = QLabel("---- AnyPosMultiCompleteEdit ----")
        mainLayout.addWidget(anyposMultiCompHeader)
        anyMultiCompDesc = QLabel("Type day of week")
        mainLayout.addWidget(anyMultiCompDesc)
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        anyposMultiLine = lineedit.AnyPosMultiCompleteEdit(days, parent = self)
        mainLayout.addWidget(anyposMultiLine)


    def changeCheckButtonDirection(self, d):
        if d == "v":
            self.checkBtnGroup.setDirection(QBoxLayout.TopToBottom)
        else:
            self.checkBtnGroup.setDirection(QBoxLayout.LeftToRight)


    def checkBtnGrpToggleEvent(self):
        if self.checkBtnGroup.isDescriptionVisible():
            self.checkBtnGroup.hideDescription()
        else:
            self.checkBtnGroup.showDescription()




if __name__ == '__main__':
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    ui = exampleGUI()
    ui.show()
    app.exec_()