from PyQt5 import QtWidgets, QtGui, QtCore
import Values_File, string, Cryptodome.Random.random
import sqlite3 as data_base

class New_db(QtWidgets.QWidget):
    def __init__(self, main_window, paren=None):
        super().__init__(paren)
        self.initUI()
        self.main_window = main_window

    def initUI(self):

        # Create widget
        self.title_namedb = QtWidgets.QLabel(Values_File.dict_lang["title_namedb"])
        self.editline_namedb = QtWidgets.QLineEdit(self)
        self.title_pswrd = QtWidgets.QLabel(Values_File.dict_lang["title_pswrd"])
        self.editline_pswrd = QtWidgets.QLineEdit(self)
        self.editline_pswrd.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.btn_ok = QtWidgets.QPushButton(Values_File.dict_lang["btn_ok"])
        self.btn_ok.setDisabled(True)

        # Create action widget
        self.editline_namedb.textChanged.connect(self.changer_editline)
        self.editline_pswrd.textChanged.connect(self.changer_editline)
        self.btn_ok.clicked.connect(self.click_btn_ok)

        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addWidget(self.title_namedb)
        self.vbox.addWidget(self.editline_namedb)
        self.vbox.addWidget(self.title_pswrd)
        self.vbox.addWidget(self.editline_pswrd)
        self.vbox.addWidget(self.btn_ok)

        # Setup window
        self.setLayout(self.vbox)
        self.setMinimumSize(260, 150)
        self.setWindowTitle('Maturym Secret')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.move_center()

    def move_center(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        form = self.geometry()
        x_move_step = (screen.width() - form.width()) / 2
        y_move_step = (screen.height() - form.height()) / 2
        self.move(int(x_move_step), int(y_move_step))

    def changer_editline(self):
        if self.editline_namedb.text() == '' or self.editline_pswrd.text() == '':
            self.btn_ok.setDisabled(True)
        else:
            self.btn_ok.setEnabled(True)

    def click_btn_ok(self):
        Values_File.create_db(self.editline_namedb.text(), Values_File.hash_pswrd(self.editline_pswrd.text()))
        self.close()

    def closeEvent(self, event):
        self.editline_namedb.setText('')
        self.editline_pswrd.setText('')

class Add_data_db(QtWidgets.QWidget):

    def __init__(self, main_window, paren=None):
        super().__init__(paren)
        self.initUI()
        self.main_window = main_window

    def initUI(self):

        # Create widget
        self.title_header = QtWidgets.QLabel(Values_File.dict_lang["title_header"])
        self.title_login = QtWidgets.QLabel(Values_File.dict_lang["title_login"])
        self.title_pswrd = QtWidgets.QLabel(Values_File.dict_lang["title_pswrd"])
        self.title_url = QtWidgets.QLabel(Values_File.dict_lang["title_url"])
        self.title_note = QtWidgets.QLabel(Values_File.dict_lang["title_note"])
        self.editline_header = QtWidgets.QLineEdit(self)
        self.editline_login = QtWidgets.QLineEdit(self)
        self.editline_pswrd = QtWidgets.QLineEdit(self)
        self.editline_url = QtWidgets.QLineEdit(self)
        self.editline_note = QtWidgets.QLineEdit(self)
        self.btn_ok = QtWidgets.QPushButton(Values_File.dict_lang["btn_ok"])
        self.btn_save = QtWidgets.QPushButton(Values_File.dict_lang["btn_save"])
        self.btn_save.hide()
        self.btn_ok.setDisabled(True)
        self.btn_cancel = QtWidgets.QPushButton(Values_File.dict_lang["btn_cancel"])

        # Create action widget
        self.editline_header.textChanged.connect(self.changer_editline)
        self.editline_login.textChanged.connect(self.changer_editline)
        self.editline_pswrd.textChanged.connect(self.changer_editline)
        self.editline_url.textChanged.connect(self.changer_editline)
        self.editline_note.textChanged.connect(self.changer_editline)
        self.btn_ok.clicked.connect(self.click_ok)
        self.btn_save.clicked.connect(self.click_save)
        self.btn_cancel.clicked.connect(self.click_cancel)

        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addWidget(self.title_header)
        self.vbox.addWidget(self.editline_header)
        self.vbox.addWidget(self.title_login)
        self.vbox.addWidget(self.editline_login)
        self.vbox.addWidget(self.title_pswrd)
        self.vbox.addWidget(self.editline_pswrd)
        self.vbox.addWidget(self.title_url)
        self.vbox.addWidget(self.editline_url)
        self.vbox.addWidget(self.title_note)
        self.vbox.addWidget(self.editline_note)

        self.hBox_btn = QtWidgets.QHBoxLayout()
        self.hBox_btn.addStretch(0)
        self.hBox_btn.addWidget(self.btn_ok)
        self.hBox_btn.addWidget(self.btn_save)
        self.hBox_btn.addWidget(self.btn_cancel)
        self.vbox.addLayout(self.hBox_btn)

        # Setup window
        self.setLayout(self.vbox)
        self.setMinimumSize(300, 300)
        self.setWindowTitle('Maturym Secret')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.move_center()

    def move_center(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        form = self.geometry()
        x_move_step = (screen.width() - form.width()) / 2
        y_move_step = (screen.height() - form.height()) / 2
        self.move(int(x_move_step), int(y_move_step))


    def changer_editline(self):
        if self.editline_header.text() == '' or self.editline_login.text() == '' or self.editline_pswrd.text() == '' or self.editline_url.text() == '' or self.editline_note.text() == '':
            self.btn_ok.setDisabled(True)
        else:
            self.btn_ok.setEnabled(True)

    def click_ok(self):
        db = data_base.connect(Values_File.directory[0])
        cursor = db.cursor()

        header = self.editline_header.text()
        login = self.editline_login.text()
        pwsd = Values_File.encrypt(self.editline_pswrd.text(), Values_File.password)
        url = self.editline_url.text()
        note = self.editline_note.text()

        request = 'INSERT INTO Storage (header, login, password, url, note) VALUES (?,?,?,?,?)'
        cursor.execute(request,(header,login,pwsd,url,note))

        db.commit()
        cursor.close()
        db.close()

        self.editline_header.setText(''), self.editline_login.setText(''), self.editline_pswrd.setText(''), self.editline_url.setText(''), self.editline_note.setText('')

        self.main_window.upd_table()
        self.close()

    def click_save(self):
        db = data_base.connect(Values_File.directory[0])
        cursor = db.cursor()

        header = self.editline_header.text()
        login = self.editline_login.text()
        pwsd = Values_File.encrypt(self.editline_pswrd.text(), Values_File.password)
        url = self.editline_url.text()
        note = self.editline_note.text()

        data = (header,login,pwsd,url,note)
        if data != Values_File.data_record[0]:
            request = 'UPDATE Storage SET login=?, password=?, url=?, note=? WHERE header=?'
            cursor.execute(request,(login,pwsd,url,note,header))

        db.commit()
        self.main_window.upd_table()
        self.editline_header.setReadOnly(False)
        cursor.close()
        db.close()

        self.editline_header.setText(''), self.editline_login.setText(''), self.editline_pswrd.setText(''), self.editline_url.setText(''), self.editline_note.setText('')
        self.btn_save.hide()
        self.btn_ok.show()
        self.close()


    def click_cancel(self):
        self.editline_header.setText(''), self.editline_login.setText(''), self.editline_pswrd.setText(''), self.editline_url.setText(''), self.editline_note.setText('')
        if self.btn_ok.show():
            self.editline_header.setReadOnly(False)
        else:
            self.btn_save.hide()
            self.btn_ok.show()
            self.editline_header.setReadOnly(False)

        self.close()

    def closeEvent(self, event):
        self.editline_header.setText(''), self.editline_login.setText(''), self.editline_pswrd.setText(''), self.editline_url.setText(''), self.editline_note.setText('')
        self.editline_header.setReadOnly(False)
        self.btn_save.hide()
        self.btn_ok.show()

class EnterPassword(QtWidgets.QWidget):
    def __init__(self, main_window, paren=None):
        super().__init__(paren)
        self.initUI()
        self.main_window = main_window

    def initUI(self):

        # Create widget
        self.title_pswrd = QtWidgets.QLabel(Values_File.dict_lang["title_pswrd"])
        self.edit_pswrd = QtWidgets.QLineEdit(self)
        self.edit_pswrd.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.btn_ok = QtWidgets.QPushButton(Values_File.dict_lang["btn_ok"])
        self.btn_ok.clicked.connect(self.click_ok)

        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addWidget(self.title_pswrd)
        self.vbox.addWidget(self.edit_pswrd)
        self.vbox.addWidget(self.btn_ok)

        # Setup window
        self.setLayout(self.vbox)
        self.setMinimumSize(300, 300)
        self.setWindowTitle('Maturym Secret')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.move_center()

    def move_center(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        form = self.geometry()
        x_move_step = (screen.width() - form.width()) / 2
        y_move_step = (screen.height() - form.height()) / 2
        self.move(int(x_move_step), int(y_move_step))

    def click_ok(self):
        db = data_base.connect(Values_File.directory[0])
        cursor = db.cursor()
        data = cursor.execute('SELECT password FROM Password').fetchall()[0][0]
        if Values_File.hash_pswrd(self.edit_pswrd.text()) == data:
            self.main_window.upd_table()
            self.main_window.toolbar.show()
            Values_File.password = self.edit_pswrd.text()
            self.edit_pswrd.setText('')
            self.close()
        else:
            msg = QtWidgets.QMessageBox(self)
            msg.setWindowTitle('Maturym Secret')
            msg.setWindowIcon(QtGui.QIcon('icon.png'))
            msg.setText('The entered password is not correct')
            msg.show()
            self.edit_pswrd.setText('')

    def closeEvent(self, event):
        self.edit_pswrd.setText('')

class Generator_Password(QtWidgets.QWidget):
    def __init__(self, paren=None):
        super().__init__(paren)
        self.initUI()

    def initUI(self):
        self.title_pswrd = QtWidgets.QLabel(Values_File.dict_lang["title_pswrd"])
        self.editline_pswrd = QtWidgets.QLineEdit(self)
        self.title_length = QtWidgets.QLabel(Values_File.dict_lang["title_length"])
        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.slider.setMinimum(4)
        self.slider.setMaximum(64)
        self.slider.setMaximumWidth(140)
        self.slider.valueChanged[int].connect(self.changeValue)
        self.title_slider_num = QtWidgets.QLabel('4')
        self.checkbox_AZ = QtWidgets.QCheckBox('A-Z')
        self.checkbox_AZ.toggle()
        self.checkbox_az = QtWidgets.QCheckBox('a-z')
        self.checkbox_az.toggle()
        self.checkbox_09 = QtWidgets.QCheckBox('0-9')
        self.checkbox_09.toggle()
        self.checkbox_simvol = QtWidgets.QCheckBox(f'*/|\*')
        self.btn_ok = QtWidgets.QPushButton(Values_File.dict_lang["btn_ok"])
        self.btn_ok.clicked.connect(self.click_ok)

        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addWidget(self.title_pswrd)
        self.vbox.addWidget(self.editline_pswrd)

        self.hbox_length_pswrd = QtWidgets.QHBoxLayout(self)
        self.hbox_length_pswrd.addStretch(0)
        self.hbox_length_pswrd.addWidget(self.title_length)
        self.hbox_length_pswrd.addWidget(self.slider)
        self.hbox_length_pswrd.addWidget(self.title_slider_num)

        self.vbox.addLayout(self.hbox_length_pswrd)

        self.hbox_checkbox = QtWidgets.QHBoxLayout(self)
        self.hbox_checkbox.addWidget(self.checkbox_AZ)
        self.hbox_checkbox.addWidget(self.checkbox_az)
        self.hbox_checkbox.addWidget(self.checkbox_09)
        self.hbox_checkbox.addWidget(self.checkbox_simvol)

        self.vbox.addLayout(self.hbox_checkbox)
        self.vbox.addWidget(self.btn_ok)

        # Setup window
        self.setLayout(self.vbox)
        self.setMinimumSize(300, 180)
        self.setWindowTitle('Maturym Secret')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.move_center()

    def move_center(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        form = self.geometry()
        x_move_step = (screen.width() - form.width()) / 2
        y_move_step = (screen.height() - form.height()) / 2
        self.move(int(x_move_step), int(y_move_step))

    def click_ok(self):
        self.close()

    def changeValue(self):
        length_key = int(self.slider.value())
        random_key = ''
        letters = ''
        if self.checkbox_AZ.isChecked():
            letters += string.ascii_uppercase
        if self.checkbox_az.isChecked():
            letters += string.ascii_lowercase
        if self.checkbox_09.isChecked():
            letters += string.digits
        if self.checkbox_simvol.isChecked():
            letters += string.punctuation

        for i in range(length_key):
            random_key += Cryptodome.Random.random.choice(letters)

        self.editline_pswrd.setText(random_key)
        self.title_slider_num.setText(str(self.slider.value()))

    def closeEvent(self, event):
        self.slider.setValue(4)
        self.editline_pswrd.setText('')

class AboutWindow(QtWidgets.QWidget):
    def __init__(self, paren=None):
        super().__init__(paren)
        self.initUI()

    def initUI(self):
        Info_About = Values_File.dict_lang["Info_About"]
        title_About = QtWidgets.QLabel(Info_About)

        HBox = QtWidgets.QHBoxLayout()

        HBox.addWidget(title_About)

        self.setLayout(HBox)

        framegeometry = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        framegeometry.moveCenter(centerPoint)
        self.move(framegeometry.topLeft())

        self.setFixedSize(455,135)
        self.setWindowTitle("About")
        self.setWindowIcon(QtGui.QIcon('icon.png'))