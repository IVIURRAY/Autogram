import os
from PyQt5.QtWidgets import *


class AutogramApp(QWidget):

    def __init__(self, parent=None):
        super(AutogramApp, self).__init__(parent)
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.posts_section(), 1, 0)
        mainLayout.addWidget(self.scheduler_section(), 1, 1)

        self.setLayout(mainLayout)

    def posts_section(self):
        box = QGroupBox("Posts")

        layout = QVBoxLayout()
        layout.addWidget(self.create_upload_btn())
        layout.addWidget(self.create_remove_btn())
        layout.addWidget(self.create_view_btn())
        box.setLayout(layout)

        return box

    def create_upload_btn(self):
        def on_click():
            print('Clicked upload...')
            self.uploads_popup = UploadPhotosPopup()
            self.uploads_popup.show()

        btn = QPushButton('Upload')
        btn.clicked.connect(on_click)

        return btn

    def create_remove_btn(self):
        def on_click():
            print('Clicked remove...')
            files, _ = self.open_file_dialog()

            if files:
                confirm = QMessageBox.question(self, 'Confirm?', f'Do you want to remove {len(files)} photos?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if confirm == QMessageBox.No:
                    print('Aborting removing photos...')
                    return

                archive_dir = os.path.normpath(os.getcwd() + '/.archive')
                if not os.path.exists(archive_dir):
                    print('Creating archive directory...')
                    os.mkdir(archive_dir)

            for file_path in files:
                try:
                    print(f'Deleting post: {file_path}')
                    filename = file_path.split('/')[-1]
                    os.rename(file_path, os.path.normpath(f'{archive_dir}/{filename}'))
                except Exception as e:
                    print(f'Unable to delete file: {file_path} \n{e}')

        btn = QPushButton('Remove')
        btn.clicked.connect(on_click)

        return btn

    def create_view_btn(self):
        def on_click():
            print('Clicked view...')
            files, _ = self.open_file_dialog()
            print(files)

        btn = QPushButton('View Photos')
        btn.clicked.connect(on_click)

        return btn

    def open_file_dialog(self):
        return QFileDialog.getOpenFileNames(self, 'Autogram', 'posts', 'All Files (*)')

    def scheduler_section(self):
        box = QGroupBox("Scheduler")

        layout = QVBoxLayout()
        layout.addWidget(QPushButton('Upload'))
        layout.addWidget(QPushButton('View'))
        box.setLayout(layout)

        return box


class UploadPhotosPopup(QWidget):

    def __init__(self, parent=None):
        super(UploadPhotosPopup, self).__init__(parent)
        self.chosen_image = None
        self.chosen_description = None

        self.btn_ok = QPushButton("OK")
        self.btn_ok.setEnabled(False)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.image_upload(), 1, 0)
        mainLayout.addWidget(self.description_upload(), 2, 0)
        mainLayout.addWidget(self.confirm_upload(), 3, 0)
        self.setLayout(mainLayout)

    def image_upload(self):
        box = QGroupBox("Image")
        btn = QPushButton("Chose Image...")
        label = QLabel('No image selected')

        def on_click():
            file, _ = self.open_file_dialog()
            print(f'Chosen image: {file}')
            label.setText(file.split('/')[-1])
            self.btn_ok.setEnabled(True)
            self.chosen_image = file

        btn.clicked.connect(on_click)

        layout = QVBoxLayout()
        layout.addWidget(btn)
        layout.addWidget(label)
        box.setLayout(layout)

        return box

    def description_upload(self):
        box = QGroupBox("Description")

        def on_change():
            self.chosen_description = textbox.toPlainText()

        textbox = QPlainTextEdit(QWidget().resize(150, 40))
        textbox.textChanged.connect(on_change)

        layout = QVBoxLayout()
        layout.addWidget(textbox)
        box.setLayout(layout)

        return box

    def confirm_upload(self):
        box = QGroupBox("Upload")

        def on_ok():
            print(f'Chosen image is: {self.chosen_image}')
            print(f'Chosen description is: {self.chosen_description}')
            self.close()

        self.btn_ok.clicked.connect(on_ok)

        layout = QHBoxLayout()
        layout.addWidget(self.btn_ok)
        layout.addWidget(QPushButton("Cancel"))
        box.setLayout(layout)

        return box

    def open_file_dialog(self):
        return QFileDialog.getOpenFileName(self, 'Autogram', 'posts', 'All Files (*)')




if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    autogram = AutogramApp()
    autogram.show()
    sys.exit(app.exec_())

