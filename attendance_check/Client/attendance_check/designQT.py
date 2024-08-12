# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\kaz\Desktop\G02\designQT.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
number = '1000000'

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1056, 633)
        font = QtGui.QFont()
        font.setPointSize(18)
        Form.setFont(font)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(120, 90, 801, 71))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(330, 280, 341, 86))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.dateLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.dateLabel.setFont(font)
        self.dateLabel.setObjectName("dateLabel")
        self.gridLayout.addWidget(self.dateLabel, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.numberLabel = QtWidgets.QLabel(self.layoutWidget)
        self.numberLabel.setObjectName("numberLabel")
        self.gridLayout.addWidget(self.numberLabel, 1, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(440, 500, 161, 20))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Form)
        self.lineEdit.returnPressed.connect(self.returnNumber)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def returnNumber(self):
        global number
        number = self.lineEdit.text()
        print(self.lineEdit.text())

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:36pt;\">学生証をかざしてください</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:18pt;\">日付：</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:18pt;\">学籍番号：</span></p></body></html>"))
        self.numberLabel.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:18pt;\">--------</span></p></body></html>"))
