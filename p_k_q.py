from PyQt5 import QtGui, QtCore, QtWidgets
import shelve
import traceback
import sys
from save_page import SavePage


fieldnames = ('source', 'login', 'password', 'any more info')
# labels and also keys for keeper dictionary
keeper = {}

class StackedWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.main_page = QtWidgets.QStackedWidget(self)
        self.main_page.resize(400, 300)

        self.setWindowTitle('Password Keeper')
        #self.setWindowIcon(QtWidgets.QIcon('favicon.ico'))
        #self.resize(600, 500)

        label = QtWidgets.QLabel('Load Page', self)
        label.setAlignment(QtCore.Qt.AlignCenter)

        # main layout
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(label)
        self.setLayout(vbox)

        hbox = QtWidgets.QHBoxLayout()  # for s_list and buttons
        vbox.addLayout(hbox)


        #source list
        source_box = QtWidgets.QVBoxLayout()
        hbox.addLayout(source_box)

        with shelve.open('shelvefile_new') as source_list:
            self.model_list = QtCore.QStringListModel(list(source_list))
            self.source_list = QtWidgets.QListView()
            self.source_list.setModel(self.model_list)
            source_box.addWidget(self.source_list)

        #buttons
        button_box = QtWidgets.QVBoxLayout()
        hbox.addLayout(button_box)
        add_new = QtWidgets.QPushButton('Add New', self)
        add_new.clicked.connect(self.add_window)
        load_button = QtWidgets.QPushButton('Load Info', self)
        load_button.clicked.connect(self.load_function)
        copy_login_button = QtWidgets.QPushButton('Copy Login', self)
        copy_login_button.clicked.connect(lambda: self.copy_info_function('login'))
        copy_password_button = QtWidgets.QPushButton('Copy Password', self)
        copy_password_button.clicked.connect(lambda: self.copy_info_function('password'))
        refresh_button = QtWidgets.QPushButton('Refresh', self)
        refresh_button.clicked.connect(self.refresh_function)
        delete_button = QtWidgets.QPushButton('Delete', self)
        delete_button.clicked.connect(self.delete_function)

        for button in (copy_login_button, copy_password_button,
                       load_button, refresh_button, delete_button, add_new):
            button_box.addWidget(button)

        self.show()

    def add_window(self):
        print("hello")
        modal = SavePage(self.main_page)

    def load_function(self):

        self.index = self.source_list.currentIndex()
        self.source = self.index.data(0)

        holder = {}
        modalWindow = QtWidgets.QWidget(self, QtCore.Qt.Window)
        modalWindow.setWindowTitle("Load info")
        #modalWindow.resize(200, 50)
        modalWindow.setWindowModality(QtCore.Qt.WindowModal)
        modalWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        main_layout = QtWidgets.QVBoxLayout(modalWindow)
        #modalWindow.setLayout(main_layout)

        try:
            db = shelve.open('shelvefile_new')
            record = db[self.source]
        except:
            traceback.print_exc()


        for i, field in enumerate(fieldnames):  # enumerate returns (index, value) tuple
            lab = QtWidgets.QLabel(field, self)  # smart
            ent = QtWidgets.QLineEdit(self)  # pretty

            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(lab)
            hbox.addWidget(ent)
            main_layout.addLayout(hbox)

            holder[field] = ent
            holder[field].clear()
            holder[field].setText(record[field])
        modalWindow.show()

    def refresh_function(self):
        try:
            with shelve.open('shelvefile_new') as db:
                self.model_list.setStringList(list(db))
        except:
            traceback.print_exc()

    def copy_info_function(self, info='login'):

        self.index = self.source_list.currentIndex()
        self.source = self.index.data(0)
        print(self.source, info)
        with shelve.open('shelvefile_new') as db:
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(db[self.source][info])
            QtWidgets.QMessageBox.information(self, 'Information',
                                          '{} of {} has been added to clipboard'.format(info, self.source))

    def delete_function(self):
        self.index = self.source_list.currentIndex()
        self.source = self.index.data(0)
        with shelve.open('shelvefile_new') as db:
            if QtWidgets.QMessageBox.question(self.source_list,
                                            'Delete Source?',
                                            'Source name is {}'.format(self.source),
                                            buttons=QtWidgets.QMessageBox.Yes |
                                            QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
                del db[self.source]
                QtWidgets.QMessageBox.information(self, 'Information',
                                          '{} has been deleted'.format(self.source))



app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('favicon.ico'))
win = StackedWindow()
sys.exit(app.exec_())