import sys, os, json
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtWidgets import QWidget, QMessageBox

from classes import UserInput
from gui.ui_wefor import Ui_MainWidget


WINDOW_WIDTH_MIN: int = 530
WINDOW_HEIGHT_FIX: int = 310


class Worker(QThread):
    error_signal = Signal(str)
    done_signal = Signal(str)

    def __init__(self, callback, user: UserInput):
        super().__init__()
        self.callback = callback
        self.args = user

    def run(self):
        try:
            self.callback(self.args)
        except Exception as e:
            self.error_signal.emit(str(e))
        else:
            self.done_signal.emit("Format Process Complete")


class OutputStreamHandler(QObject):
    text_output = Signal(str)

    def write(self, text):
        self.text_output.emit(str(text))

    def flush(self):
        pass


class MainWidget(QWidget, Ui_MainWidget):
    @property
    def config_file(self) -> str:
        return "settings.json"

    def __init__(self, callback):
        super().__init__()
        self.setupUi(self)
        self.callback = callback
        self.user = UserInput("none")
        self.do_LoadSettings()

        self.setFixedSize(WINDOW_WIDTH_MIN, WINDOW_HEIGHT_FIX)

        self.in_dir_button.clicked.connect(self.set_Input)
        self.in_dir_edit.textChanged.connect(self.set_Output)
        self.out_dir_button.clicked.connect(self.set_ManualOutput)
        self.auto_output_check.clicked.connect(self.set_Output)

        self.min_panel_h_val.valueChanged.connect(lambda: self.set_Arguments("min_height"))
        self.tolerance_val.valueChanged.connect(lambda: self.set_Arguments("tolerance"))

        self.type_auto.clicked.connect(lambda: self.set_Arguments("i_type", "auto"))
        self.type_main.clicked.connect(lambda: self.set_Arguments("i_type", "main"))
        self.type_sub.clicked.connect(lambda: self.set_Arguments("i_type", "chapter"))

        self.page_direction_right.clicked.connect(lambda: self.set_Arguments("direction", "right"))
        self.page_direction_left.clicked.connect(lambda: self.set_Arguments("direction", "left"))
        self.save_config_button.clicked.connect(self.do_SaveSettings)
        self.process_button.clicked.connect(self.do_FormatProcess)

        sys.stdout = OutputStreamHandler()
        sys.stdout.text_output.connect(self.do_DisplayPrint)

    def __del__(self):
        sys.stdout = sys.__stdout__

    def do_LoadSettings(self) -> None:
        try:
            with open(self.config_file, 'r') as file:
                settings = json.load(file)
                self.user.input_type = settings["input_type"]
                self.user.direction = settings["direction"]
                self.user.tolerance = settings["tolerance"]
                self.user.min_height_p = settings["min_panel_height"]
                auto_output = settings["auto_output"]
        except (FileNotFoundError, json.JSONDecodeError):
            auto_output = True
            self.do_SaveSettings()

        self.auto_output_check.setChecked(auto_output)
        match self.user.input_type:
            case "auto":
                self.type_auto.setChecked(True)
            case "main":
                self.type_main.setChecked(True)
            case "sub":
                self.type_sub.setChecked(True)

        match self.user.direction:
            case "right":
                self.page_direction_right.setChecked(True)
            case "left":
                self.page_direction_left.setChecked(True)

        self.tolerance_val.setValue(self.user.tolerance)
        self.min_panel_h_val.setValue(self.user.min_height_p)

    def do_SaveSettings(self) -> None:
        settings = {
            "input_type": self.user.input_type,
            "tolerance": self.user.tolerance,
            "min_panel_height": self.user.min_height_p,
            "direction": self.user.direction,
            "auto_output": self.auto_output_check.isChecked()
        }
        with open(self.config_file, 'w') as file:
            json.dump(settings, file)

    def set_Arguments(self, type: str, value: str = "") -> None:
        match type:
            case "i_type":
                self.user.input_type = value
            case "direction":
                self.user.direction = value
            case "min_height":
                self.user.min_height_p = self.min_panel_h_val.value()
                self.status_box.setText(f"Min Panel Height set to: {self.user.min_height_p:.2f}")
            case "tolerance":
                self.user.tolerance = self.tolerance_val.value()
                self.status_box.setText(f"Tolerance set to: {self.user.tolerance}")
            case _:
                pass

    def do_DisplayPrint(self, msg: str) -> None:
        if msg != "\n":
            self.status_box.setText(msg)
    
    def set_Input(self) -> None:
        self.in_dir_edit.clear()
        self.in_dir_edit.paste()

    def set_Output(self, paste: bool = False) -> None:
        self.out_dir_edit.clear()
        if self.auto_output_check.isChecked():
            self.out_dir_edit.setText(os.path.join(self.in_dir_edit.text(), "_output"))
        elif paste:
            self.out_dir_edit.paste()
    
    def set_ManualOutput(self) -> None:
        self.auto_output_check.setChecked(False)
        self.set_Output(paste=True)

    def do_VerifyInput(self, process: bool = False) -> None:
        if not self.in_dir_edit.text():
            raise ValueError("Input directory cannot be empty")

        if not os.path.exists(self.in_dir_edit.text()):
            raise ValueError("Input directory does not exist")
        
        if not self.out_dir_edit.text():
            raise ValueError("Output directory cannot be empty")

        if process:
            self.user.input_dir = self.in_dir_edit.text()
            self.user.output_dir = self.out_dir_edit.text()
            if not os.path.exists(self.user.output_dir):
                ret = QMessageBox.warning(self, "Output directory does not exist",
                                                "Output directory does not exist. Do you want to create it?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                                QMessageBox.StandardButton.No)
                if ret == QMessageBox.StandardButton.No:
                    raise ValueError("Please select different output directory")

    def do_FormatProcess(self) -> None:
        try:
            self.do_VerifyInput(process=True)
        except ValueError as err:
            QMessageBox.critical(self, "Error", str(err), QMessageBox.StandardButton.Ok)
            return

        self.worker = Worker(callback=self.callback, user=self.user)
        self.worker.done_signal.connect(self.on_Finished)
        self.worker.error_signal.connect(self.on_Error)
        self.process_button.setEnabled(False)
        self.worker.start()

    def on_Finished(self, msg: str) -> None:
        QMessageBox.information(self, "Complete", msg, QMessageBox.StandardButton.Ok)
        self.process_button.setEnabled(True)
        print("READY!")

    def on_Error(self, err: str) -> None:
        QMessageBox.critical(self, "Error", err, QMessageBox.StandardButton.Ok)
        self.process_button.setEnabled(True)
