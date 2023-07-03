from PyQt5 import QtWidgets, QtGui
import sqlite3 as data_base
import sys, Values_File, SecondWindow, pyperclip

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.New_db_window = SecondWindow.New_db(self)
        self.Add_data_db_window = SecondWindow.Add_data_db(self)
        self.About_window = SecondWindow.AboutWindow()
        self.Enter_pswrd_window = SecondWindow.EnterPassword(main_window=self)
        self.Generator_Password = SecondWindow.Generator_Password()

        self.new_db = QtWidgets.QAction(QtGui.QIcon(r'Icons folder\new_db.png'),Values_File.dict_lang["new_db"], self)
        self.new_db.triggered.connect(self.new_db_action)
        self.open_db = QtWidgets.QAction(QtGui.QIcon(r'Icons folder\open_db.png'),Values_File.dict_lang["open_db"], self)
        self.open_db.triggered.connect(self.open_db_action)
        self.close_db = QtWidgets.QAction(QtGui.QIcon(r'Icons folder\close_db.png'),Values_File.dict_lang["close_db"], self)
        self.close_db.triggered.connect(self.close_db_action)
        self.info = QtWidgets.QAction(QtGui.QIcon(r'Icons folder\about.png'),Values_File.dict_lang["info"], self)
        self.info.triggered.connect(self.info_action)
        self.lang = QtWidgets.QAction(QtGui.QIcon(r'Icons folder\language.png'),Values_File.dict_lang["lang"], self)
        self.lang.triggered.connect(self.lang_action)

        self.new_note = QtWidgets.QAction(QtGui.QIcon(r'Icons folder\new_note.png'), Values_File.dict_lang["new_note"], self)
        self.new_note.triggered.connect(self.new_note_action)
        self.edit_note = QtWidgets.QAction(QtGui.QIcon(r'Icons folder\edit_note.png'), Values_File.dict_lang["edit_note"], self)
        self.edit_note.triggered.connect(self.edit_data)
        self.delete_note = QtWidgets.QAction(QtGui.QIcon(r'Icons folder\delete_note.png'), Values_File.dict_lang["delete_note"], self)
        self.delete_note.triggered.connect(self.delete_data)
        self.copy_username = QtWidgets.QAction(QtGui.QIcon(r'Icons folder\copy_username.png'), Values_File.dict_lang["copy_username"], self)
        self.copy_username.triggered.connect(self.copy_usernames)
        self.copy_password = QtWidgets.QAction(QtGui.QIcon(r'Icons folder\copy_password.png'), Values_File.dict_lang["copy_password"], self)
        self.copy_password.triggered.connect(self.copy_passwords)
        self.block_db = QtWidgets.QAction(QtGui.QIcon(r'Icons folder\block_db.png'), Values_File.dict_lang["block_db"], self)
        self.block_db.triggered.connect(self.block_dbase)
        self.key_generation = QtWidgets.QAction(QtGui.QIcon(r'Icons folder\key_generation.png'), Values_File.dict_lang["key_generation"], self)
        self.key_generation.triggered.connect(self.generator_password)
        self.find_in_db = QtWidgets.QAction(QtGui.QIcon(r'Icons folder\find.png'), 'Find', self)

        self.filemenu = self.menuBar().addMenu(Values_File.dict_lang["filemenu"])
        self.filemenu.addAction(self.new_db)
        self.filemenu.addAction(self.open_db)
        self.filemenu.addAction(self.close_db)

        self.aboutmenu = self.menuBar().addMenu(Values_File.dict_lang["aboutmenu"])
        self.aboutmenu.addAction(self.info)
        self.aboutmenu.addAction(self.lang)

        self.toolbar = self.addToolBar('tools')
        self.toolbar.addAction(self.new_note)
        self.toolbar.addAction(self.edit_note)
        self.toolbar.addAction(self.delete_note)
        self.toolbar.addAction(self.copy_username)
        self.toolbar.addAction(self.copy_password)
        self.toolbar.addAction(self.block_db)
        self.toolbar.addAction(self.key_generation)
        self.toolbar.addAction(self.find_in_db)
        self.toolbar.hide()

        self.Vbox = QtWidgets.QVBoxLayout()

        self.table_widget = QtWidgets.QTableWidget(self)
        self.table_widget.setSortingEnabled(Values_File.Sorting_Enabled)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(Values_File.Header_Labels)
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.widget_Hbox = QtWidgets.QWidget(self)

        self.Vbox.addWidget(self.table_widget)
        self.widget_Hbox.setLayout(self.Vbox)
        self.setCentralWidget(self.widget_Hbox)

        self.setMinimumSize(480, 500)
        self.setWindowTitle('Maturym Secret')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.move_center()

    def move_center(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        form = self.geometry()
        x_move_step = (screen.width() - form.width()) / 2
        y_move_step = (screen.height() - form.height()) / 2
        self.move(int(x_move_step), int(y_move_step))

    # menubar clik option

    def new_db_action(self):
        self.New_db_window.show()

    def open_db_action(self):
        Values_File.directory = QtWidgets.QFileDialog.getOpenFileName(None,'Open file','', 'Data base files (*.db)')
        print(Values_File.directory)
        if Values_File.directory != ('', ''):
            self.Enter_pswrd_window.show()
        else: print('not find file')

    def close_db_action(self):
        self.table_widget.clear()
        self.table_widget.setHorizontalHeaderLabels(Values_File.Header_Labels)
        self.table_widget.setRowCount(0)
        self.toolbar.hide()
        Values_File.directory = ''

    def info_action(self):
        self.About_window.show()

    def lang_action(self):
        self.InputDialog = QtWidgets.QInputDialog(self)
        data = self.InputDialog.getItem(self,'Maturym Secret',Values_File.dict_lang["Get_lang"], Values_File.keys_data)
        Values_File.lang = data[0]
        Values_File.write_lang_config()

    #toolbar clik option

    def new_note_action(self):
        self.Add_data_db_window.show()

    def upd_table(self):
        db = data_base.connect(Values_File.directory[0])
        cursor = db.cursor()
        data = cursor.execute('SELECT header, login, url FROM Storage').fetchall()

        self.table_widget.setRowCount(len(data))

        row = 0
        for i in data:
            col = 0
            for item in i:
                cell = QtWidgets.QTableWidgetItem(item)
                self.table_widget.setItem(row, col, cell)
                col += 1
            row += 1

        cursor.close()
        db.close()

    def edit_data(self):
        db = data_base.connect(Values_File.directory[0])
        cursor = db.cursor()
        request = 'SELECT * FROM Storage WHERE header=?'
        row = self.table_widget.currentIndex().row()
        colm = 0
        text = self.table_widget.item(row,colm).text()
        Values_File.data_record = cursor.execute(request, (text,)).fetchall()
        self.Add_data_db_window.show()
        self.Add_data_db_window.editline_header.setText(Values_File.data_record[0][0])
        self.Add_data_db_window.editline_header.setReadOnly(True)
        self.Add_data_db_window.editline_login.setText(Values_File.data_record[0][1])
        self.Add_data_db_window.editline_pswrd.setText(Values_File.decrypt(Values_File.data_record[0][2],Values_File.password))
        self.Add_data_db_window.editline_url.setText(Values_File.data_record[0][3])
        self.Add_data_db_window.editline_note.setText(Values_File.data_record[0][4])
        self.Add_data_db_window.btn_ok.hide()
        self.Add_data_db_window.btn_save.show()
        cursor.close()
        db.close()

    def delete_data(self):
        db = data_base.connect(Values_File.directory[0])
        cursor = db.cursor()
        request = 'DELETE FROM Storage WHERE header=?'
        row = self.table_widget.currentIndex().row()
        colm = 0
        text = self.table_widget.item(row, colm).text()
        cursor.execute(request, (text,))
        db.commit()
        cursor.close()
        db.close()
        self.upd_table()

    def copy_usernames(self):
        row = self.table_widget.currentIndex().row()
        colm = 1
        text = self.table_widget.item(row, colm).text()
        pyperclip.copy(text)

    def copy_passwords(self):
        db = data_base.connect(Values_File.directory[0])
        cursor = db.cursor()
        row = self.table_widget.currentIndex().row()
        colm = 0
        text = self.table_widget.item(row, colm).text()
        request = 'SELECT password FROM Storage WHERE header=?'
        data = cursor.execute(request,(text,)).fetchall()
        db.commit()
        cursor.close()
        db.close()
        pyperclip.copy(Values_File.decrypt(data[0][0], Values_File.password))

    def block_dbase(self):
        self.table_widget.clear()
        self.table_widget.setHorizontalHeaderLabels(Values_File.Header_Labels)
        self.table_widget.setRowCount(0)
        self.toolbar.hide()

        self.Enter_pswrd_window.show()

    def generator_password(self):
        self.Generator_Password.show()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    Window = MainWindow()
    Window.show()
    sys.exit(app.exec_())