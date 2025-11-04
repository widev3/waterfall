# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dashboard.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
    QAbstractScrollArea,
    QApplication,
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(1042, 726)
        font = QFont()
        font.setFamilies(["Wix Madefor Display"])
        Dialog.setFont(font)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonFileOpen = QPushButton(Dialog)
        self.pushButtonFileOpen.setObjectName("pushButtonFileOpen")
        self.pushButtonFileOpen.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButtonFileOpen.setIconSize(QSize(25, 25))

        self.gridLayout.addWidget(self.pushButtonFileOpen, 0, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollAreaView = QScrollArea(self.frame)
        self.scrollAreaView.setObjectName("scrollAreaView")
        self.scrollAreaView.setMinimumSize(QSize(300, 0))
        self.scrollAreaView.setMaximumSize(QSize(300, 16777215))
        self.scrollAreaView.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.scrollAreaView.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scrollAreaView.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )
        self.scrollAreaView.setWidgetResizable(True)
        self.scrollAreaWidgetContentsView = QWidget()
        self.scrollAreaWidgetContentsView.setObjectName("scrollAreaWidgetContentsView")
        self.scrollAreaWidgetContentsView.setGeometry(QRect(0, 0, 284, 653))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContentsView)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_5 = QFrame(self.scrollAreaWidgetContentsView)
        self.frame_5.setObjectName("frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_11 = QGridLayout(self.frame_5)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.labelOffsetsView = QLabel(self.frame_5)
        self.labelOffsetsView.setObjectName("labelOffsetsView")

        self.gridLayout_11.addWidget(self.labelOffsetsView, 0, 0, 1, 1)

        self.label_2 = QLabel(self.frame_5)
        self.label_2.setObjectName("label_2")

        self.gridLayout_11.addWidget(self.label_2, 1, 0, 1, 1)

        self.horizontalSliderGammaView = QSlider(self.frame_5)
        self.horizontalSliderGammaView.setObjectName("horizontalSliderGammaView")
        self.horizontalSliderGammaView.setMaximum(1000)
        self.horizontalSliderGammaView.setSingleStep(1)
        self.horizontalSliderGammaView.setPageStep(50)
        self.horizontalSliderGammaView.setSliderPosition(500)
        self.horizontalSliderGammaView.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_11.addWidget(self.horizontalSliderGammaView, 1, 1, 1, 1)

        self.labelGammaView = QLabel(self.frame_5)
        self.labelGammaView.setObjectName("labelGammaView")

        self.gridLayout_11.addWidget(self.labelGammaView, 1, 2, 1, 1)

        self.comboBoxOffsetsView = QComboBox(self.frame_5)
        self.comboBoxOffsetsView.setObjectName("comboBoxOffsetsView")

        self.gridLayout_11.addWidget(self.comboBoxOffsetsView, 0, 1, 1, 2)

        self.verticalLayout.addWidget(self.frame_5)

        self.verticalSpacer_4 = QSpacerItem(
            0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.frame_6 = QFrame(self.scrollAreaWidgetContentsView)
        self.frame_6.setObjectName("frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_12 = QGridLayout(self.frame_6)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.label_11 = QLabel(self.frame_6)
        self.label_11.setObjectName("label_11")

        self.gridLayout_12.addWidget(self.label_11, 2, 0, 1, 1)

        self.lineEditFPwr = QLineEdit(self.frame_6)
        self.lineEditFPwr.setObjectName("lineEditFPwr")
        self.lineEditFPwr.setReadOnly(True)

        self.gridLayout_12.addWidget(self.lineEditFPwr, 2, 2, 1, 1)

        self.lineEditFilename = QLineEdit(self.frame_6)
        self.lineEditFilename.setObjectName("lineEditFilename")
        self.lineEditFilename.setReadOnly(True)

        self.gridLayout_12.addWidget(self.lineEditFilename, 0, 2, 1, 1)

        self.label_9 = QLabel(self.frame_6)
        self.label_9.setObjectName("label_9")

        self.gridLayout_12.addWidget(self.label_9, 1, 0, 1, 1)

        self.label = QLabel(self.frame_6)
        self.label.setObjectName("label")

        self.gridLayout_12.addWidget(self.label, 0, 0, 1, 1)

        self.lineEditTPwr = QLineEdit(self.frame_6)
        self.lineEditTPwr.setObjectName("lineEditTPwr")
        self.lineEditTPwr.setReadOnly(True)

        self.gridLayout_12.addWidget(self.lineEditTPwr, 1, 2, 1, 1)

        self.label_20 = QLabel(self.frame_6)
        self.label_20.setObjectName("label_20")

        self.gridLayout_12.addWidget(self.label_20, 1, 3, 1, 1)

        self.label_21 = QLabel(self.frame_6)
        self.label_21.setObjectName("label_21")

        self.gridLayout_12.addWidget(self.label_21, 2, 3, 1, 1)

        self.verticalLayout.addWidget(self.frame_6)

        self.scrollAreaView.setWidget(self.scrollAreaWidgetContentsView)

        self.gridLayout_2.addWidget(self.scrollAreaView, 0, 0, 1, 1)

        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.framePlotsView = QFrame(Dialog)
        self.framePlotsView.setObjectName("framePlotsView")
        self.framePlotsView.setFrameShape(QFrame.Shape.StyledPanel)
        self.gridLayout_3 = QGridLayout(self.framePlotsView)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalSpacer_4 = QSpacerItem(
            0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 2, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(
            0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout_3.addItem(self.verticalSpacer_2, 1, 0, 1, 1)

        self.verticalLayoutFreq = QVBoxLayout()
        self.verticalLayoutFreq.setObjectName("verticalLayoutFreq")

        self.gridLayout_3.addLayout(self.verticalLayoutFreq, 0, 2, 1, 1)

        self.verticalLayoutSpec = QVBoxLayout()
        self.verticalLayoutSpec.setObjectName("verticalLayoutSpec")

        self.gridLayout_3.addLayout(self.verticalLayoutSpec, 0, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(
            0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout_3.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.verticalLayoutTime = QVBoxLayout()
        self.verticalLayoutTime.setObjectName("verticalLayoutTime")

        self.gridLayout_3.addLayout(self.verticalLayoutTime, 1, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(
            0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_3.addItem(self.horizontalSpacer_5, 2, 2, 1, 1)

        self.gridLayout.addWidget(self.framePlotsView, 1, 1, 1, 1)

        QWidget.setTabOrder(self.comboBoxOffsetsView, self.horizontalSliderGammaView)
        QWidget.setTabOrder(self.horizontalSliderGammaView, self.lineEditFilename)
        QWidget.setTabOrder(self.lineEditFilename, self.lineEditTPwr)
        QWidget.setTabOrder(self.lineEditTPwr, self.lineEditFPwr)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(
            QCoreApplication.translate("Dialog", "Wide3 Waterfall", None)
        )
        self.pushButtonFileOpen.setText(
            QCoreApplication.translate("Dialog", "File open", None)
        )
        self.labelOffsetsView.setText(
            QCoreApplication.translate("Dialog", "TextLabel", None)
        )
        self.label_2.setText(QCoreApplication.translate("Dialog", "gamma", None))
        self.labelGammaView.setText(
            QCoreApplication.translate("Dialog", "TextLabel", None)
        )
        self.label_11.setText(QCoreApplication.translate("Dialog", "f. pwr", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", "t. pwr", None))
        self.label.setText(QCoreApplication.translate("Dialog", "Filename", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", "\u00b5W", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", "\u00b5W", None))

    # retranslateUi
