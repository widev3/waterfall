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
    QGroupBox,
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
        self.scrollAreaWidgetContentsView.setGeometry(QRect(0, 0, 284, 651))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContentsView)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_gamma = QGroupBox(self.scrollAreaWidgetContentsView)
        self.groupBox_gamma.setObjectName("groupBox_gamma")
        self.gridLayout_4 = QGridLayout(self.groupBox_gamma)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.labelOffsetsView = QLabel(self.groupBox_gamma)
        self.labelOffsetsView.setObjectName("labelOffsetsView")

        self.gridLayout_4.addWidget(self.labelOffsetsView, 0, 0, 1, 1)

        self.horizontalSliderGammaView = QSlider(self.groupBox_gamma)
        self.horizontalSliderGammaView.setObjectName("horizontalSliderGammaView")
        self.horizontalSliderGammaView.setMaximum(1000)
        self.horizontalSliderGammaView.setSingleStep(1)
        self.horizontalSliderGammaView.setPageStep(50)
        self.horizontalSliderGammaView.setSliderPosition(500)
        self.horizontalSliderGammaView.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_4.addWidget(self.horizontalSliderGammaView, 2, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox_gamma)
        self.label_2.setObjectName("label_2")

        self.gridLayout_4.addWidget(self.label_2, 2, 0, 1, 1)

        self.labelGammaView = QLabel(self.groupBox_gamma)
        self.labelGammaView.setObjectName("labelGammaView")

        self.gridLayout_4.addWidget(self.labelGammaView, 2, 2, 1, 1)

        self.comboBoxOffsetsView = QComboBox(self.groupBox_gamma)
        self.comboBoxOffsetsView.setObjectName("comboBoxOffsetsView")

        self.gridLayout_4.addWidget(self.comboBoxOffsetsView, 0, 1, 1, 2)

        self.verticalLayout.addWidget(self.groupBox_gamma)

        self.groupBox_signals = QGroupBox(self.scrollAreaWidgetContentsView)
        self.groupBox_signals.setObjectName("groupBox_signals")
        self.gridLayout_5 = QGridLayout(self.groupBox_signals)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.pushButtonSignal1 = QPushButton(self.groupBox_signals)
        self.pushButtonSignal1.setObjectName("pushButtonSignal1")

        self.gridLayout_5.addWidget(self.pushButtonSignal1, 0, 0, 1, 1)

        self.pushButtonSignal2 = QPushButton(self.groupBox_signals)
        self.pushButtonSignal2.setObjectName("pushButtonSignal2")

        self.gridLayout_5.addWidget(self.pushButtonSignal2, 1, 0, 1, 1)

        self.verticalLayout.addWidget(self.groupBox_signals)

        self.verticalSpacer_4 = QSpacerItem(
            0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.groupBox_file = QGroupBox(self.scrollAreaWidgetContentsView)
        self.groupBox_file.setObjectName("groupBox_file")
        self.gridLayout_6 = QGridLayout(self.groupBox_file)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label = QLabel(self.groupBox_file)
        self.label.setObjectName("label")

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)

        self.label_9 = QLabel(self.groupBox_file)
        self.label_9.setObjectName("label_9")

        self.gridLayout_6.addWidget(self.label_9, 1, 0, 1, 1)

        self.lineEditTPwr = QLineEdit(self.groupBox_file)
        self.lineEditTPwr.setObjectName("lineEditTPwr")
        self.lineEditTPwr.setReadOnly(True)

        self.gridLayout_6.addWidget(self.lineEditTPwr, 1, 1, 1, 1)

        self.label_20 = QLabel(self.groupBox_file)
        self.label_20.setObjectName("label_20")

        self.gridLayout_6.addWidget(self.label_20, 1, 2, 1, 1)

        self.label_11 = QLabel(self.groupBox_file)
        self.label_11.setObjectName("label_11")

        self.gridLayout_6.addWidget(self.label_11, 2, 0, 1, 1)

        self.lineEditFPwr = QLineEdit(self.groupBox_file)
        self.lineEditFPwr.setObjectName("lineEditFPwr")
        self.lineEditFPwr.setReadOnly(True)

        self.gridLayout_6.addWidget(self.lineEditFPwr, 2, 1, 1, 1)

        self.label_21 = QLabel(self.groupBox_file)
        self.label_21.setObjectName("label_21")

        self.gridLayout_6.addWidget(self.label_21, 2, 2, 1, 1)

        self.lineEditFilename = QLineEdit(self.groupBox_file)
        self.lineEditFilename.setObjectName("lineEditFilename")
        self.lineEditFilename.setReadOnly(True)

        self.gridLayout_6.addWidget(self.lineEditFilename, 0, 1, 1, 2)

        self.verticalLayout.addWidget(self.groupBox_file)

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

        self.verticalLayoutTotal = QVBoxLayout()
        self.verticalLayoutTotal.setObjectName("verticalLayoutTotal")

        self.gridLayout_3.addLayout(self.verticalLayoutTotal, 1, 2, 1, 1)

        self.gridLayout.addWidget(self.framePlotsView, 1, 1, 1, 1)

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
        self.groupBox_gamma.setTitle(
            QCoreApplication.translate("Dialog", "Gamma", None)
        )
        self.labelOffsetsView.setText(
            QCoreApplication.translate("Dialog", "TextLabel", None)
        )
        self.label_2.setText(QCoreApplication.translate("Dialog", "gamma", None))
        self.labelGammaView.setText(
            QCoreApplication.translate("Dialog", "TextLabel", None)
        )
        self.groupBox_signals.setTitle(
            QCoreApplication.translate("Dialog", "Signals", None)
        )
        self.pushButtonSignal1.setText(
            QCoreApplication.translate("Dialog", "PushButton", None)
        )
        self.pushButtonSignal2.setText(
            QCoreApplication.translate("Dialog", "PushButton", None)
        )
        self.groupBox_file.setTitle(QCoreApplication.translate("Dialog", "File", None))
        self.label.setText(QCoreApplication.translate("Dialog", "Filename", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", "t. pwr", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", "\u00b5W", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", "f. pwr", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", "\u00b5W", None))

    # retranslateUi
