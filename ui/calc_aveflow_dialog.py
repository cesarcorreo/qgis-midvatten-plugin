# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calc_aveflow_dialog.ui'
#
# Created: Thu Jan 23 20:13:31 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.setEnabled(True)
        Dialog.resize(493, 268)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        Dialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Dialog.setModal(False)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.Instructions = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Instructions.sizePolicy().hasHeightForWidth())
        self.Instructions.setSizePolicy(sizePolicy)
        self.Instructions.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.Instructions.setFont(font)
        self.Instructions.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.Instructions.setWordWrap(True)
        self.Instructions.setIndent(3)
        self.Instructions.setObjectName(_fromUtf8("Instructions"))
        self.verticalLayout.addWidget(self.Instructions)
        self.line = QtGui.QFrame(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        self.line.setFont(font)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setIndent(3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.FromDateTime = QtGui.QDateTimeEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FromDateTime.sizePolicy().hasHeightForWidth())
        self.FromDateTime.setSizePolicy(sizePolicy)
        self.FromDateTime.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.FromDateTime.setFont(font)
        self.FromDateTime.setWrapping(False)
        self.FromDateTime.setFrame(True)
        self.FromDateTime.setSpecialValueText(_fromUtf8(""))
        self.FromDateTime.setKeyboardTracking(True)
        self.FromDateTime.setDateTime(QtCore.QDateTime(QtCore.QDate(1901, 1, 1), QtCore.QTime(0, 0, 0)))
        self.FromDateTime.setCalendarPopup(True)
        self.FromDateTime.setObjectName(_fromUtf8("FromDateTime"))
        self.horizontalLayout.addWidget(self.FromDateTime)
        self.label_3 = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setIndent(3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.ToDateTime = QtGui.QDateTimeEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ToDateTime.sizePolicy().hasHeightForWidth())
        self.ToDateTime.setSizePolicy(sizePolicy)
        self.ToDateTime.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.ToDateTime.setFont(font)
        self.ToDateTime.setWrapping(False)
        self.ToDateTime.setFrame(True)
        self.ToDateTime.setSpecialValueText(_fromUtf8(""))
        self.ToDateTime.setKeyboardTracking(True)
        self.ToDateTime.setDateTime(QtCore.QDateTime(QtCore.QDate(2099, 12, 31), QtCore.QTime(23, 59, 59)))
        self.ToDateTime.setCalendarPopup(True)
        self.ToDateTime.setObjectName(_fromUtf8("ToDateTime"))
        self.horizontalLayout.addWidget(self.ToDateTime)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_2 = QtGui.QFrame(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        self.line_2.setFont(font)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.label = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_All = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_All.sizePolicy().hasHeightForWidth())
        self.pushButton_All.setSizePolicy(sizePolicy)
        self.pushButton_All.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.pushButton_All.setFont(font)
        self.pushButton_All.setObjectName(_fromUtf8("pushButton_All"))
        self.horizontalLayout_2.addWidget(self.pushButton_All)
        self.pushButton_Selected = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Selected.sizePolicy().hasHeightForWidth())
        self.pushButton_Selected.setSizePolicy(sizePolicy)
        self.pushButton_Selected.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.pushButton_Selected.setFont(font)
        self.pushButton_Selected.setObjectName(_fromUtf8("pushButton_Selected"))
        self.horizontalLayout_2.addWidget(self.pushButton_Selected)
        self.pushButton_Cancel = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Cancel.sizePolicy().hasHeightForWidth())
        self.pushButton_Cancel.setSizePolicy(sizePolicy)
        self.pushButton_Cancel.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.pushButton_Cancel.setFont(font)
        self.pushButton_Cancel.setObjectName(_fromUtf8("pushButton_Cancel"))
        self.horizontalLayout_2.addWidget(self.pushButton_Cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.Instructions.setText(QtGui.QApplication.translate("Dialog", "Average flow (l/s) is about to be calculated and stored in table w_flow (parameter=\'Aveflow\'). For the calculation, all values of accumulated volume (\'Accvol\') are assumed to be given in m3. Any existing values of \'Aveflow\' will be left unchanged and only such values that are not already present in the database will be added. \n"
"\n"
"Aveflow is to be calculated for Accvol observations within this interval:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "From:", None, QtGui.QApplication.UnicodeUTF8))
        self.FromDateTime.setDisplayFormat(QtGui.QApplication.translate("Dialog", "yyyy-MM-dd HH:mm:ss", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "To:", None, QtGui.QApplication.UnicodeUTF8))
        self.ToDateTime.setDisplayFormat(QtGui.QApplication.translate("Dialog", "yyyy-MM-dd HH:mm:ss", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Do you want \'Aveflow\' to be calculated for all or only the selected objects? (The question is only about obsid. Aveflow will always be calculated for ALL instrumentids for the selected obsid.)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_All.setText(QtGui.QApplication.translate("Dialog", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Selected.setText(QtGui.QApplication.translate("Dialog", "Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Cancel.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
