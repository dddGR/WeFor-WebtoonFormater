# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'wefor.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpinBox, QVBoxLayout, QWidget)

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        if not MainWidget.objectName():
            MainWidget.setObjectName(u"MainWidget")
        MainWidget.resize(530, 310)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWidget.sizePolicy().hasHeightForWidth())
        MainWidget.setSizePolicy(sizePolicy)
        self.user_input_advance = QGroupBox(MainWidget)
        self.user_input_advance.setObjectName(u"user_input_advance")
        self.user_input_advance.setGeometry(QRect(10, 97, 511, 141))
        self.verticalLayout_7 = QVBoxLayout(self.user_input_advance)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, 5, -1, -1)
        self.uia_layout = QGridLayout()
        self.uia_layout.setObjectName(u"uia_layout")
        self.uia_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.input_type_box = QGroupBox(self.user_input_advance)
        self.input_type_box.setObjectName(u"input_type_box")
        self.verticalLayout_4 = QVBoxLayout(self.input_type_box)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(16, -1, -1, -1)
        self.input_type_layout = QVBoxLayout()
        self.input_type_layout.setObjectName(u"input_type_layout")
        self.type_auto = QRadioButton(self.input_type_box)
        self.type_auto.setObjectName(u"type_auto")

        self.input_type_layout.addWidget(self.type_auto)

        self.type_main = QRadioButton(self.input_type_box)
        self.type_main.setObjectName(u"type_main")

        self.input_type_layout.addWidget(self.type_main)

        self.type_sub = QRadioButton(self.input_type_box)
        self.type_sub.setObjectName(u"type_sub")

        self.input_type_layout.addWidget(self.type_sub)


        self.verticalLayout_4.addLayout(self.input_type_layout)


        self.uia_layout.addWidget(self.input_type_box, 0, 1, 2, 1)

        self.tolerance_box = QGroupBox(self.user_input_advance)
        self.tolerance_box.setObjectName(u"tolerance_box")
        self.verticalLayout_6 = QVBoxLayout(self.tolerance_box)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(32, 5, 32, 5)
        self.tolerance_val = QSpinBox(self.tolerance_box)
        self.tolerance_val.setObjectName(u"tolerance_val")
        self.tolerance_val.setMinimum(1)
        self.tolerance_val.setMaximum(255)

        self.verticalLayout_6.addWidget(self.tolerance_val)


        self.uia_layout.addWidget(self.tolerance_box, 0, 3, 1, 1)

        self.page_direction_box = QGroupBox(self.user_input_advance)
        self.page_direction_box.setObjectName(u"page_direction_box")
        self.verticalLayout_3 = QVBoxLayout(self.page_direction_box)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(16, -1, -1, -1)
        self.pd_layout = QVBoxLayout()
        self.pd_layout.setObjectName(u"pd_layout")
        self.page_direction_left = QRadioButton(self.page_direction_box)
        self.page_direction_left.setObjectName(u"page_direction_left")

        self.pd_layout.addWidget(self.page_direction_left)

        self.page_direction_right = QRadioButton(self.page_direction_box)
        self.page_direction_right.setObjectName(u"page_direction_right")

        self.pd_layout.addWidget(self.page_direction_right)


        self.verticalLayout_3.addLayout(self.pd_layout)


        self.uia_layout.addWidget(self.page_direction_box, 0, 2, 2, 1)

        self.min_panel_h_box = QGroupBox(self.user_input_advance)
        self.min_panel_h_box.setObjectName(u"min_panel_h_box")
        self.verticalLayout_5 = QVBoxLayout(self.min_panel_h_box)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(32, 5, 32, 5)
        self.min_panel_h_val = QDoubleSpinBox(self.min_panel_h_box)
        self.min_panel_h_val.setObjectName(u"min_panel_h_val")
        self.min_panel_h_val.setMaximum(100.000000000000000)
        self.min_panel_h_val.setSingleStep(0.100000000000000)

        self.verticalLayout_5.addWidget(self.min_panel_h_val)


        self.uia_layout.addWidget(self.min_panel_h_box, 1, 3, 1, 1)

        self.auto_output_box = QGroupBox(self.user_input_advance)
        self.auto_output_box.setObjectName(u"auto_output_box")
        self.auto_output_box.setLayoutDirection(Qt.LeftToRight)
        self.auto_output_box.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.verticalLayout = QVBoxLayout(self.auto_output_box)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(16, -1, -1, -1)
        self.auto_output_check = QCheckBox(self.auto_output_box)
        self.auto_output_check.setObjectName(u"auto_output_check")
        self.auto_output_check.setEnabled(True)

        self.verticalLayout.addWidget(self.auto_output_check)


        self.uia_layout.addWidget(self.auto_output_box, 0, 4, 1, 1)

        self.save_config_button = QPushButton(self.user_input_advance)
        self.save_config_button.setObjectName(u"save_config_button")
        self.save_config_button.setMaximumSize(QSize(80, 16777215))

        self.uia_layout.addWidget(self.save_config_button, 1, 4, 1, 1)


        self.verticalLayout_7.addLayout(self.uia_layout)

        self.layoutWidget = QWidget(MainWidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 241, 511, 61))
        self.user_process = QHBoxLayout(self.layoutWidget)
        self.user_process.setObjectName(u"user_process")
        self.user_process.setContentsMargins(0, 0, 0, 0)
        self.status_box = QLabel(self.layoutWidget)
        self.status_box.setObjectName(u"status_box")
        self.status_box.setFrameShape(QFrame.NoFrame)
        self.status_box.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)
        self.status_box.setMargin(12)

        self.user_process.addWidget(self.status_box)

        self.process_button = QPushButton(self.layoutWidget)
        self.process_button.setObjectName(u"process_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.process_button.sizePolicy().hasHeightForWidth())
        self.process_button.setSizePolicy(sizePolicy1)
        self.process_button.setMaximumSize(QSize(90, 60))
        self.process_button.setBaseSize(QSize(0, 0))

        self.user_process.addWidget(self.process_button)

        self.layoutWidget1 = QWidget(MainWidget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 11, 511, 73))
        self.user_input_basic = QGridLayout(self.layoutWidget1)
        self.user_input_basic.setObjectName(u"user_input_basic")
        self.user_input_basic.setContentsMargins(0, 0, 0, 0)
        self.out_dir_label = QLabel(self.layoutWidget1)
        self.out_dir_label.setObjectName(u"out_dir_label")

        self.user_input_basic.addWidget(self.out_dir_label, 1, 0, 1, 1)

        self.in_dir_edit = QLineEdit(self.layoutWidget1)
        self.in_dir_edit.setObjectName(u"in_dir_edit")

        self.user_input_basic.addWidget(self.in_dir_edit, 0, 1, 1, 1)

        self.out_dir_edit = QLineEdit(self.layoutWidget1)
        self.out_dir_edit.setObjectName(u"out_dir_edit")

        self.user_input_basic.addWidget(self.out_dir_edit, 1, 1, 1, 1)

        self.in_dir_button = QPushButton(self.layoutWidget1)
        self.in_dir_button.setObjectName(u"in_dir_button")
        self.in_dir_button.setMaximumSize(QSize(60, 16777215))

        self.user_input_basic.addWidget(self.in_dir_button, 0, 2, 1, 1)

        self.out_dir_button = QPushButton(self.layoutWidget1)
        self.out_dir_button.setObjectName(u"out_dir_button")
        self.out_dir_button.setMaximumSize(QSize(60, 16777215))

        self.user_input_basic.addWidget(self.out_dir_button, 1, 2, 1, 1)

        self.in_dir_label = QLabel(self.layoutWidget1)
        self.in_dir_label.setObjectName(u"in_dir_label")

        self.user_input_basic.addWidget(self.in_dir_label, 0, 0, 1, 1)


        self.retranslateUi(MainWidget)

        QMetaObject.connectSlotsByName(MainWidget)
    # setupUi

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(QCoreApplication.translate("MainWidget", u"Webtoon Formatter", None))
        self.user_input_advance.setTitle(QCoreApplication.translate("MainWidget", u"Advance Options", None))
        self.input_type_box.setTitle(QCoreApplication.translate("MainWidget", u"Input Type", None))
        self.type_auto.setText(QCoreApplication.translate("MainWidget", u"Auto", None))
        self.type_main.setText(QCoreApplication.translate("MainWidget", u"Main", None))
        self.type_sub.setText(QCoreApplication.translate("MainWidget", u"Chapter", None))
        self.tolerance_box.setTitle(QCoreApplication.translate("MainWidget", u"Tolerance [1-255]", None))
        self.page_direction_box.setTitle(QCoreApplication.translate("MainWidget", u"Page Direction", None))
        self.page_direction_left.setText(QCoreApplication.translate("MainWidget", u"Left > Right", None))
        self.page_direction_right.setText(QCoreApplication.translate("MainWidget", u"Right > Left", None))
        self.min_panel_h_box.setTitle(QCoreApplication.translate("MainWidget", u"Min Panel Height [%]", None))
        self.auto_output_box.setTitle(QCoreApplication.translate("MainWidget", u"Output", None))
        self.auto_output_check.setText(QCoreApplication.translate("MainWidget", u"Auto", None))
        self.save_config_button.setText(QCoreApplication.translate("MainWidget", u"Save Settings", None))
        self.status_box.setText(QCoreApplication.translate("MainWidget", u"READY", None))
        self.process_button.setText(QCoreApplication.translate("MainWidget", u"FORMAT", None))
        self.out_dir_label.setText(QCoreApplication.translate("MainWidget", u"Output Directory:", None))
        self.in_dir_edit.setText("")
        self.in_dir_edit.setPlaceholderText(QCoreApplication.translate("MainWidget", u"Put Your Webtoon Directory Here", None))
        self.out_dir_edit.setPlaceholderText(QCoreApplication.translate("MainWidget", u"Put Your Output Here", None))
        self.in_dir_button.setText(QCoreApplication.translate("MainWidget", u"Paste", None))
        self.out_dir_button.setText(QCoreApplication.translate("MainWidget", u"Paste", None))
        self.in_dir_label.setText(QCoreApplication.translate("MainWidget", u"Input Directory:", None))
    # retranslateUi

