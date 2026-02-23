# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'computer.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QGridLayout,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(1636, 993)
        font = QFont()
        font.setFamilies(["Wix Madefor Display"])
        Dialog.setFont(font)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 2)

        self.framePlotsView = QFrame(Dialog)
        self.framePlotsView.setObjectName("framePlotsView")
        self.framePlotsView.setFrameShape(QFrame.Shape.StyledPanel)
        self.gridLayout_3 = QGridLayout(self.framePlotsView)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 2, 2)

        self.gridLayout.addWidget(self.framePlotsView, 1, 0, 1, 2)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(
            QCoreApplication.translate("Dialog", "Wide3 Waterfall", None)
        )

    # retranslateUi
