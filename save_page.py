from PyQt5 import QtWidgets, QtCore, QtWidgets
import shelve

fieldnames = ('source', 'login', 'password', 'any more info')
keeper = {}

class SavePage(QtWidgets.QWidget):

    def __init__(self, parent=None, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.Window)
        self.parent = parent

        label = QtWidgets.QLabel('Save Page', self)
        label.setAlignment(QtCore.Qt.AlignCenter)

        # main layout
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(label)
        self.setLayout(vbox)

        for i, field in enumerate(fieldnames):  # enumerate returns (index, value) tuple
            lab = QtWidgets.QLabel(field, self)  # smart
            ent = QtWidgets.QLineEdit(self)  # pretty

            ent.setWidth(300)

            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(lab)
            hbox.addWidget(ent)
            vbox.addLayout(hbox)

            keeper[field] = ent  # why not ent.get? because Lutz did same

        #save and back buttons
        button_layout = QtWidgets.QHBoxLayout()
        save_button = QtWidgets.QPushButton('Save', self)
        save_button.clicked.connect(self.save_function)
        button_layout.addWidget(save_button)
        vbox.addLayout(button_layout)

        
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.show()


    def save_function(self):
        db = shelve.open('shelvefile_new')  # open the file
        source = keeper['source'].text()  # key for info
        if source in db:
            for field in fieldnames:
                keeper[field].clear()
            QtWidgets.QMessageBox.information(self, 'Information',
                                          'Already have {}'.format(source),
                                          buttons=QtWidgets.QMessageBox.Close,
                                          defaultButton=QtWidgets.QMessageBox.Close)

        elif source == '':
            QtWidgets.QMessageBox.information(self, 'Information',
                "empty source key is not allowed")

        else:
            record = dict()
            for field in fieldnames:
                record[field] = keeper[field].text()
            db[source] = record  # db = {source: record}

            save_name = open('NameBase.txt', 'a')  # for list in LoadPage
            save_name.write(source + '\n')
            save_name.close()

            for field in fieldnames:
                keeper[field].clear()
            QtWidgets.QMessageBox.information(self, 'Info',
                                          'Data has been saved')

        db.close()
        self.close()
