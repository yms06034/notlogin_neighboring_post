import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
import main_logic_code as api
from ui import Ui_MainWindow
from datetime import datetime

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

main_ui = Ui_MainWindow()

NAME = "Naver neighbor's new comment"

class SeleniumThread(QThread):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal() 

    def __init__(self, main_window ,contents_list=None):
        super().__init__()
        self.contents_list = contents_list
        self.main_window = main_window
        self._running = True

    def run(self):
        id = main_ui.id.text()
        pwd = main_ui.pwd.text()

        if id:
            pass
        else:
            self.log_signal.emit("아이디를 입력해주세요.")
        
        if pwd:
            pass
        else:
            self.log_signal.emit("비밀번호를 입력해주세요.")

        if self.contents_list:
            pass
        else:
            self.log_signal.emit("작성할 원고를 넣어주세요.")

        for i in self.contents_list:
            print(i)
            print("--" * 5)
        
        if all([id, pwd, self.contents_list]):
            try:
                self.log_signal.emit("프로그램을 시작합니다.")
                self.browser = api.open_browser()
                api.naver_login(id, pwd, self.browser)
                if self.browser.current_url == 'https://nid.naver.com/nidlogin.login':
                    self.browser.close()
                    self.log_signal.emit(f'{id} 아이디로 로그인에 실패하였습니다. \t\n로그인 정보를 다시 확인해주세요.')
                    self.browser = None
                    return
                api.neighborhood_new_post(self.browser, self.contents_list)
            except Exception as ex:
                self.log_signal.emit("프로그램이 정상적으로 종료되었습니다.")
                return
            finally:
                self.finished_signal.emit()

        
    def stop(self):
        self._running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main_ui.setupUi(self)

        window_ico = resource_path('favicon.ico')
        self.setWindowIcon(QIcon(window_ico))

        self.timer = QTimer(self)

        self.setWindowTitle("Naver neighbor's new comment")
        self.browser = None

        self.contents_list = []
        self.selenium_thread = None

        main_ui.pushButton.clicked.connect(self.btn_addCmtClicked) # Txt file Import button
        main_ui.pushButton_2.clicked.connect(self.btn_delCmtClicked) # Txt file Delete button

        main_ui.btn_start.clicked.connect(self.start_btn) # Login Start button

        main_ui.textEdit.setReadOnly(True)

    def btn_addCmtClicked(self):
        path = QFileDialog.getOpenFileNames(self)
        for p in path[0]:
            if p == '':
                return 
            if not p.lower().endswith('.txt'):
                QMessageBox.information(self, NAME, ".txt 확장자만 넣을 수 있습니다. \t\n파일 확장자를 다시 확인해주세요.")
                return
            
            file = open(p, 'rt', encoding='UTF8')
            contents = file.read()
            file.close()

            filename = os.path.basename(p)
            print(filename)

            main_ui.contents.addItem(filename)
            self.contents_list.append(contents)

    
    def btn_delCmtClicked(self):
        option = QMessageBox.warning(self, NAME, "원고를 삭제하시겠습니까?", QMessageBox.Yes | QMessageBox.No)
        if option == QMessageBox.Yes:
            if main_ui.contents.currentItem():
                tmp = main_ui.contents.currentRow()
                main_ui.contents.takeItem(main_ui.contents.currentRow())
                self.contents_list.remove(self.contents_list[tmp])
        return
    
    def start_btn(self):
        try:
            self.selenium_thread = SeleniumThread(self, self.contents_list)
            self.selenium_thread.log_signal.connect(self.update_log)
            self.selenium_thread.start()
        except Exception as e:
            print(e)

    def thread_finished(self):  
        self.selenium_thread = None  
    
    def closeEvent(self, event):  
        if self.selenium_thread is not None and self.selenium_thread.isRunning():
            self.selenium_thread.stop()
            self.selenium_thread.wait()

    def update_log(self, message):
        main_ui.textEdit.append(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())