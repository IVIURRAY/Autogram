import os
import shutil
import uuid

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

import instagram
import config
import scheduler


def setup():
    if not os.path.exists(config.TEMP_DIR):
        os.mkdir(config.TEMP_DIR)
    if not os.path.exists(config.POSTS_DIR):
        os.mkdir(config.POSTS_DIR)


def open_files_dialog(qwidget):
    return QFileDialog.getOpenFileNames(qwidget, 'Autogram', config.POSTS_DIR, 'All Files (*)')


def open_file_dialog(qwidget):
    return QFileDialog.getOpenFileName(qwidget, 'Autogram', config.POSTS_DIR, 'All Files (*)')


class AutogramApp(QWidget):

    def __init__(self, parent=None):
        setup()
        super(AutogramApp, self).__init__(parent)

        # Other windows
        self.add_photos_popup = AddPhotosPopup()
        self.instagram_login_popup = InstagramLoginPopup()
        self.instagram_login_popup.got_username.connect(self.receive_username)
        self.instagram_login_popup.got_password.connect(self.receive_password)

        # Buttons
        self.btn_add_photos = QPushButton('Add')
        self.btn_remove_photos = QPushButton('Remove')
        self.btn_view_photos = QPushButton('View')
        self.btn_upload_to_instagram = QPushButton("Upload Now")
        self.btn_login_instagram = QPushButton('Login')
        self.btn_upload_to_instagram.setEnabled(False)

        # Helpers
        self.scheduler = scheduler.Scheduler()
        self.autogram = instagram.Autogram(config.DEFAULT_USERNAME, config.DEFAULT_PASSWORD)  # TODO - This needs to start headless.

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.posts_section(), 1, 0)
        mainLayout.addWidget(self.scheduler_section(), 1, 1)

        self.setMinimumWidth(250)
        self.setWindowTitle("Autogram")
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
            self.add_photos_popup.show()

        self.btn_add_photos.clicked.connect(on_click)

        return self.btn_add_photos

    def create_remove_btn(self):
        def on_click():
            print('Clicked remove...')
            files, _ = open_files_dialog(self)

            if files:
                confirm = QMessageBox.question(self, 'Confirm?', f'Do you want to remove {len(files)} photos?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if confirm == QMessageBox.No:
                    print('Aborting removing photos...')
                    return
                self.toggle_photo_buttons(False)

                if not os.path.exists(config.ARCHIVE_DIR):
                    print('Creating archive directory...')
                    os.mkdir(config.ARCHIVE_DIR)

            for file_path in files:
                try:
                    print(f'Deleting post: {file_path}')
                    filename, extension = file_path.split('/')[-1].split('.')
                    os.rename(file_path, os.path.normpath(f'{config.ARCHIVE_DIR}/{filename}_{uuid.uuid4()}.{extension}'))
                    self.scheduler.remove_schedule_for_post(f'{filename}.{extension}')
                except Exception as e:
                    print(f'Unable to delete file: {file_path} \n{e}')

            self.toggle_photo_buttons(True)

        self.btn_remove_photos.clicked.connect(on_click)

        return self.btn_remove_photos

    def create_view_btn(self):
        def on_click():
            self.view_posts_popup = ViewPhotosPopup()  # create a new one so we don't get stale reads of the posts dir
            self.view_posts_popup.show()

        self.btn_view_photos.clicked.connect(on_click)

        return self.btn_view_photos

    def toggle_photo_buttons(self, enabled):
        self.btn_add_photos.setEnabled(enabled)
        self.btn_remove_photos.setEnabled(enabled)
        self.btn_view_photos.setEnabled(enabled)

    def scheduler_section(self):
        box = QGroupBox("Scheduler")

        self.btn_login_instagram.clicked.connect(self.on_click_instagram_login)
        self.btn_upload_to_instagram.clicked.connect(self.on_click_instagram_upload)
        layout = QVBoxLayout()
        layout.addWidget(self.btn_login_instagram)
        layout.addWidget(self.btn_upload_to_instagram)
        box.setLayout(layout)

        return box

    def on_click_instagram_login(self):
        self.instagram_login_popup.show()

    def on_click_instagram_upload(self):
        file, _ = open_file_dialog(self)
        if file:
            schedule = self.scheduler.get_schedule_for_post(file.split('/')[-1])
            if schedule:
                self.autogram._auto_post(schedule['photo'], schedule['description'])

    def receive_username(self, usr):
        self.autogram.set_username(usr)

    def receive_password(self, pwd):
        self.autogram.set_password(pwd)
        self.btn_upload_to_instagram.setEnabled(True)


class ViewPhotosPopup(QWidget):

    def __init__(self, parent=None):
        super(ViewPhotosPopup, self).__init__(parent)
        self.setWindowTitle('Autogram - Image Viewer')
        self.setMinimumWidth(700)
        self.setMinimumHeight(700)
        self.initUI()

    def create_photo_stream(self):
        for post in os.listdir(config.POSTS_DIR):
            post_path = os.path.normpath(f'{config.POSTS_DIR}/{post}')
            pixmap = QPixmap(post_path)
            label = QLabel(pixmap=pixmap)
            self.scroll_area_content.addWidget(label)

    def initUI(self):
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        widget = QWidget()
        self.scroll_area.setWidget(widget)
        self.scroll_area_content = QVBoxLayout(widget)
        self.layout_All = QVBoxLayout(self)
        self.layout_All.addWidget(self.scroll_area)
        self.create_photo_stream()


class InstagramLoginPopup(QWidget):

    got_username = QtCore.pyqtSignal(str)
    got_password = QtCore.pyqtSignal(str)

    def __init__(self, parnet=None):
        super(InstagramLoginPopup, self).__init__(parnet)
        self._username = None
        self._password = None
        self.setMinimumWidth(250)
        self.setWindowTitle("IG Login")

        self.btn_login = QPushButton("Login")
        self.input_username = QLineEdit()
        self.input_password = QLineEdit()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.username(), 1, 0)
        mainLayout.addWidget(self.password(), 2, 0)
        mainLayout.addWidget(self.confirm(), 3, 0)
        self.setLayout(mainLayout)

    def username(self):
        box = QGroupBox("Enter Username")
        layout = QVBoxLayout()
        self.input_username.resize(200, 40)
        layout.addWidget(self.input_username)
        box.setLayout(layout)

        return box

    def password(self):
        box = QGroupBox("Enter Password")
        layout = QVBoxLayout()
        self.input_password.resize(200, 40)
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_password)
        box.setLayout(layout)

        return box

    def confirm(self):
        box = QGroupBox("Login")
        layout = QVBoxLayout()
        self.btn_login.clicked.connect(self.on_click_login)
        layout.addWidget(self.btn_login)
        box.setLayout(layout)

        return box

    def on_click_login(self):
        print('USERNAME: ', self.input_username.text())
        print('PWD: ', self.input_password.displayText())
        self.got_username.emit(self.input_username.text())
        self.got_password.emit(self.input_password.text())
        self.close()


class AddPhotosPopup(QWidget):

    def __init__(self, parent=None):
        super(AddPhotosPopup, self).__init__(parent)
        self.chosen_image = None
        self.chosen_description = None

        self.btn_ok = QPushButton("OK")
        self.btn_ok.setEnabled(False)
        self.chosen_image_label = QLabel('No image selected')
        self.description_textbox = QPlainTextEdit(QWidget().resize(150, 40))

        self.scheduler = scheduler.Scheduler()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.image_upload(), 1, 0)
        mainLayout.addWidget(self.description_upload(), 2, 0)
        mainLayout.addWidget(self.confirm_upload(), 3, 0)
        self.setLayout(mainLayout)

    def image_upload(self):
        box = QGroupBox("Image")
        btn = QPushButton("Chose Image...")

        def on_click():
            file, _ = self.open_file_dialog()
            self.chosen_image_label.setText(file.split('/')[-1])
            self.btn_ok.setEnabled(True)
            self.chosen_image = file

        btn.clicked.connect(on_click)

        layout = QVBoxLayout()
        layout.addWidget(btn)
        layout.addWidget(self.chosen_image_label)
        box.setLayout(layout)

        return box

    def description_upload(self):
        box = QGroupBox("Description")

        def on_change():
            self.chosen_description = self.description_textbox.toPlainText()

        self.description_textbox.textChanged.connect(on_change)

        layout = QVBoxLayout()
        layout.addWidget(self.description_textbox)
        box.setLayout(layout)

        return box

    def confirm_upload(self):
        box = QGroupBox("Upload")

        def on_ok():
            file_name = self.chosen_image.split('/')[-1]
            destination = os.path.normpath(f'{config.POSTS_DIR}/{file_name}')
            print(f'Moving file {self.chosen_image} to {destination}')
            try:
                shutil.copy(self.chosen_image, destination)
            except shutil.SameFileError as e:
                print(e)
                QMessageBox.critical(self, 'Duplicate File', f'Filename already exists: Please rename {file_name}',
                                     QMessageBox.Close, QMessageBox.Close)
                self.close()
                return
            self.add_photo_to_schedule()
            QMessageBox.information(self, 'Success', f'Uploaded file {file_name} successfully!', QMessageBox.Close, QMessageBox.Close)
            self.close()

        self.btn_ok.clicked.connect(on_ok)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.close)
        layout = QHBoxLayout()
        layout.addWidget(self.btn_ok)
        layout.addWidget(btn_cancel)
        box.setLayout(layout)

        return box

    def add_photo_to_schedule(self):
        print(f'Chosen image is: {self.chosen_image}')
        print(f'Chosen description is: {self.chosen_description}')
        self.scheduler.write_schedule_for_post(self.chosen_image.split('/')[-1], self.chosen_description)

    def close(self):
        self.chosen_description = None
        self.chosen_image = None
        self.chosen_image_label.setText('No image selected')
        self.description_textbox.clear()
        super().close()

    def open_file_dialog(self):
        return QFileDialog.getOpenFileName(self, 'Autogram', config.POSTS_DIR, 'All Files (*)')


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    autogram = AutogramApp()
    autogram.show()
    sys.exit(app.exec_())

