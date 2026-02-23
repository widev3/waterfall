# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dashboard.ui'
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
    QAbstractScrollArea,
    QApplication,
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(1112, 779)
        font = QFont()
        font.setFamilies(["Wix Madefor Display"])
        Dialog.setFont(font)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
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
        self.scrollAreaWidgetContentsView.setGeometry(QRect(0, -103, 300, 842))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContentsView)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButtonFileOpen = QPushButton(self.scrollAreaWidgetContentsView)
        self.pushButtonFileOpen.setObjectName("pushButtonFileOpen")
        self.pushButtonFileOpen.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButtonFileOpen.setIconSize(QSize(25, 25))

        self.verticalLayout.addWidget(self.pushButtonFileOpen)

        self.groupBox_file = QGroupBox(self.scrollAreaWidgetContentsView)
        self.groupBox_file.setObjectName("groupBox_file")
        self.gridLayout_6 = QGridLayout(self.groupBox_file)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_9 = QLabel(self.groupBox_file)
        self.label_9.setObjectName("label_9")

        self.gridLayout_6.addWidget(self.label_9, 1, 0, 1, 1)

        self.lineEditFPwr = QLineEdit(self.groupBox_file)
        self.lineEditFPwr.setObjectName("lineEditFPwr")
        self.lineEditFPwr.setReadOnly(True)

        self.gridLayout_6.addWidget(self.lineEditFPwr, 2, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox_file)
        self.label_3.setObjectName("label_3")

        self.gridLayout_6.addWidget(self.label_3, 5, 0, 1, 1)

        self.label_7 = QLabel(self.groupBox_file)
        self.label_7.setObjectName("label_7")

        self.gridLayout_6.addWidget(self.label_7, 4, 0, 1, 1)

        self.label_21 = QLabel(self.groupBox_file)
        self.label_21.setObjectName("label_21")

        self.gridLayout_6.addWidget(self.label_21, 2, 2, 1, 1)

        self.label_5 = QLabel(self.groupBox_file)
        self.label_5.setObjectName("label_5")

        self.gridLayout_6.addWidget(self.label_5, 3, 0, 1, 1)

        self.lineEditFMin = QLineEdit(self.groupBox_file)
        self.lineEditFMin.setObjectName("lineEditFMin")
        self.lineEditFMin.setReadOnly(True)

        self.gridLayout_6.addWidget(self.lineEditFMin, 5, 1, 1, 1)

        self.lineEditTPwr = QLineEdit(self.groupBox_file)
        self.lineEditTPwr.setObjectName("lineEditTPwr")
        self.lineEditTPwr.setReadOnly(True)

        self.gridLayout_6.addWidget(self.lineEditTPwr, 1, 1, 1, 1)

        self.lineEditTMax = QLineEdit(self.groupBox_file)
        self.lineEditTMax.setObjectName("lineEditTMax")
        self.lineEditTMax.setReadOnly(True)

        self.gridLayout_6.addWidget(self.lineEditTMax, 4, 1, 1, 1)

        self.label_20 = QLabel(self.groupBox_file)
        self.label_20.setObjectName("label_20")

        self.gridLayout_6.addWidget(self.label_20, 1, 2, 1, 1)

        self.label_6 = QLabel(self.groupBox_file)
        self.label_6.setObjectName("label_6")

        self.gridLayout_6.addWidget(self.label_6, 3, 2, 1, 1)

        self.label_4 = QLabel(self.groupBox_file)
        self.label_4.setObjectName("label_4")

        self.gridLayout_6.addWidget(self.label_4, 5, 2, 1, 1)

        self.label_8 = QLabel(self.groupBox_file)
        self.label_8.setObjectName("label_8")

        self.gridLayout_6.addWidget(self.label_8, 4, 2, 1, 1)

        self.label_11 = QLabel(self.groupBox_file)
        self.label_11.setObjectName("label_11")

        self.gridLayout_6.addWidget(self.label_11, 2, 0, 1, 1)

        self.lineEditTMin = QLineEdit(self.groupBox_file)
        self.lineEditTMin.setObjectName("lineEditTMin")
        self.lineEditTMin.setReadOnly(True)

        self.gridLayout_6.addWidget(self.lineEditTMin, 3, 1, 1, 1)

        self.lineEditFilename = QLineEdit(self.groupBox_file)
        self.lineEditFilename.setObjectName("lineEditFilename")
        self.lineEditFilename.setReadOnly(True)

        self.gridLayout_6.addWidget(self.lineEditFilename, 0, 1, 1, 2)

        self.label = QLabel(self.groupBox_file)
        self.label.setObjectName("label")

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)

        self.label_10 = QLabel(self.groupBox_file)
        self.label_10.setObjectName("label_10")

        self.gridLayout_6.addWidget(self.label_10, 6, 0, 1, 1)

        self.lineEditFMax = QLineEdit(self.groupBox_file)
        self.lineEditFMax.setObjectName("lineEditFMax")
        self.lineEditFMax.setReadOnly(True)

        self.gridLayout_6.addWidget(self.lineEditFMax, 6, 1, 1, 1)

        self.label_12 = QLabel(self.groupBox_file)
        self.label_12.setObjectName("label_12")

        self.gridLayout_6.addWidget(self.label_12, 6, 2, 1, 1)

        self.verticalLayout.addWidget(self.groupBox_file)

        self.groupBox = QGroupBox(self.scrollAreaWidgetContentsView)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButtonISdBm = QRadioButton(self.groupBox)
        self.radioButtonISdBm.setObjectName("radioButtonISdBm")

        self.horizontalLayout.addWidget(self.radioButtonISdBm)

        self.radioButtonISuW = QRadioButton(self.groupBox)
        self.radioButtonISuW.setObjectName("radioButtonISuW")

        self.horizontalLayout.addWidget(self.radioButtonISuW)

        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContentsView)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButtonFSLin = QRadioButton(self.groupBox_2)
        self.radioButtonFSLin.setObjectName("radioButtonFSLin")

        self.horizontalLayout_2.addWidget(self.radioButtonFSLin)

        self.radioButtonFSLog = QRadioButton(self.groupBox_2)
        self.radioButtonFSLog.setObjectName("radioButtonFSLog")

        self.horizontalLayout_2.addWidget(self.radioButtonFSLog)

        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContentsView)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.radioButtonTSLin = QRadioButton(self.groupBox_3)
        self.radioButtonTSLin.setObjectName("radioButtonTSLin")

        self.horizontalLayout_3.addWidget(self.radioButtonTSLin)

        self.radioButtonTSLog = QRadioButton(self.groupBox_3)
        self.radioButtonTSLog.setObjectName("radioButtonTSLog")

        self.horizontalLayout_3.addWidget(self.radioButtonTSLog)

        self.verticalLayout.addWidget(self.groupBox_3)

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
        self.pushButtonRemove = QPushButton(self.groupBox_signals)
        self.pushButtonRemove.setObjectName("pushButtonRemove")

        self.gridLayout_5.addWidget(self.pushButtonRemove, 1, 2, 1, 1)

        self.pushButtonAdd = QPushButton(self.groupBox_signals)
        self.pushButtonAdd.setObjectName("pushButtonAdd")

        self.gridLayout_5.addWidget(self.pushButtonAdd, 1, 0, 1, 1)

        self.pushButtonCompute = QPushButton(self.groupBox_signals)
        self.pushButtonCompute.setObjectName("pushButtonCompute")

        self.gridLayout_5.addWidget(self.pushButtonCompute, 1, 3, 1, 1)

        self.listWidgetSignals = QListWidget(self.groupBox_signals)
        self.listWidgetSignals.setObjectName("listWidgetSignals")

        self.gridLayout_5.addWidget(self.listWidgetSignals, 0, 0, 1, 4)

        self.verticalLayout.addWidget(self.groupBox_signals)

        self.verticalSpacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.scrollAreaView.setWidget(self.scrollAreaWidgetContentsView)

        self.gridLayout_2.addWidget(self.scrollAreaView, 0, 0, 1, 1)

        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.framePlotsView = QFrame(Dialog)
        self.framePlotsView.setObjectName("framePlotsView")
        self.framePlotsView.setFrameShape(QFrame.Shape.StyledPanel)
        self.gridLayout_3 = QGridLayout(self.framePlotsView)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayoutSpec = QVBoxLayout()
        self.verticalLayoutSpec.setObjectName("verticalLayoutSpec")

        self.gridLayout_3.addLayout(self.verticalLayoutSpec, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 2, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout_3.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.verticalLayoutFreq = QVBoxLayout()
        self.verticalLayoutFreq.setObjectName("verticalLayoutFreq")

        self.gridLayout_3.addLayout(self.verticalLayoutFreq, 0, 2, 1, 1)

        self.verticalLayoutTime = QVBoxLayout()
        self.verticalLayoutTime.setObjectName("verticalLayoutTime")

        self.gridLayout_3.addLayout(self.verticalLayoutTime, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout_3.addItem(self.horizontalSpacer, 2, 1, 1, 1)

        self.tabWidget = QTabWidget(self.framePlotsView)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.East)
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_7 = QGridLayout(self.tab)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.verticalLayoutTotalFreq = QVBoxLayout()
        self.verticalLayoutTotalFreq.setObjectName("verticalLayoutTotalFreq")

        self.gridLayout_7.addLayout(self.verticalLayoutTotalFreq, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_8 = QGridLayout(self.tab_2)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.verticalLayoutTotalTime = QVBoxLayout()
        self.verticalLayoutTotalTime.setObjectName("verticalLayoutTotalTime")

        self.gridLayout_8.addLayout(self.verticalLayoutTotalTime, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_3.addWidget(self.tabWidget, 1, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout_3.addItem(self.verticalSpacer_2, 0, 0, 1, 1)

        self.gridLayout.addWidget(self.framePlotsView, 0, 1, 1, 1)

        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(1)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(
            QCoreApplication.translate("Dialog", "Wide3 Waterfall", None)
        )
        self.pushButtonFileOpen.setText(
            QCoreApplication.translate("Dialog", "File open", None)
        )
        self.groupBox_file.setTitle(QCoreApplication.translate("Dialog", "File", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", "t. pwr", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", "f. min", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", "t. max", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", "\u00b5W", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", "t. min", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", "\u00b5W", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", "sec", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", "MHz", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", "sec", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", "f. pwr", None))
        self.label.setText(QCoreApplication.translate("Dialog", "Filename", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", "f. max", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", "MHz", None))
        self.groupBox.setTitle(
            QCoreApplication.translate("Dialog", "Intensity scale", None)
        )
        self.radioButtonISdBm.setText(QCoreApplication.translate("Dialog", "dBm", None))
        self.radioButtonISuW.setText(
            QCoreApplication.translate("Dialog", "\u00b5W", None)
        )
        self.groupBox_2.setTitle(
            QCoreApplication.translate("Dialog", "Frequency scale", None)
        )
        self.radioButtonFSLin.setText(
            QCoreApplication.translate("Dialog", "Linear", None)
        )
        self.radioButtonFSLog.setText(QCoreApplication.translate("Dialog", "Log", None))
        self.groupBox_3.setTitle(
            QCoreApplication.translate("Dialog", "Time scale", None)
        )
        self.radioButtonTSLin.setText(
            QCoreApplication.translate("Dialog", "Linear", None)
        )
        self.radioButtonTSLog.setText(QCoreApplication.translate("Dialog", "Log", None))
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
        self.pushButtonRemove.setText(QCoreApplication.translate("Dialog", "-", None))
        self.pushButtonAdd.setText(QCoreApplication.translate("Dialog", "+", None))
        self.pushButtonCompute.setText(
            QCoreApplication.translate("Dialog", "compute", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab),
            QCoreApplication.translate("Dialog", "Frequency", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2),
            QCoreApplication.translate("Dialog", "Time", None),
        )

    # retranslateUi
