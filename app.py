import json
import os
import shutil
import uuid
import tempfile

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

TEMP_DIR = os.path.normpath(tempfile.gettempdir() + '/Autogram')
POSTS_DIR = os.path.normpath(TEMP_DIR + '/posts')
ARCHIVE_DIR = os.path.normpath(TEMP_DIR + '/.archive')
SCHEDULE = os.path.normpath(TEMP_DIR + '/.schedule')


def setup():
    if not os.path.exists(TEMP_DIR):
        os.mkdir(TEMP_DIR)
    if not os.path.exists(POSTS_DIR):
        os.mkdir(POSTS_DIR)


class AutogramApp(QWidget):

    def __init__(self, parent=None):
        setup()
        super(AutogramApp, self).__init__(parent)

        # Other windows
        self.uploads_popup = UploadPhotosPopup()

        # Buttons
        self.btn_upload_photos = QPushButton('Upload')
        self.btn_remove_photos = QPushButton('Remove')
        self.btn_view_photos = QPushButton('View Photos')

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
            self.uploads_popup.show()

        self.btn_upload_photos.clicked.connect(on_click)

        return self.btn_upload_photos

    def create_remove_btn(self):
        def on_click():
            print('Clicked remove...')
            files, _ = self.open_remove_file_dialog()

            if files:
                confirm = QMessageBox.question(self, 'Confirm?', f'Do you want to remove {len(files)} photos?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if confirm == QMessageBox.No:
                    print('Aborting removing photos...')
                    return
                self.toggle_photo_buttons(False)

                if not os.path.exists(ARCHIVE_DIR):
                    print('Creating archive directory...')
                    os.mkdir(ARCHIVE_DIR)

            for file_path in files:
                try:
                    print(f'Deleting post: {file_path}')
                    filename, extension = file_path.split('/')[-1].split('.')
                    os.rename(file_path, os.path.normpath(f'{ARCHIVE_DIR}/{filename}_{uuid.uuid4()}.{extension}'))
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

    def open_remove_file_dialog(self):
        return QFileDialog.getOpenFileNames(self, 'Autogram', POSTS_DIR, 'All Files (*)')

    def toggle_photo_buttons(self, enabled):
        self.btn_upload_photos.setEnabled(enabled)
        self.btn_remove_photos.setEnabled(enabled)
        self.btn_view_photos.setEnabled(enabled)

    def scheduler_section(self):
        box = QGroupBox("Scheduler")

        layout = QVBoxLayout()
        # layout.addWidget(QPushButton('Upload'))
        # layout.addWidget(QPushButton('View'))
        layout.addWidget(QLabel('Coming soon.'))
        box.setLayout(layout)

        return box


class ViewPhotosPopup(QWidget):

    def __init__(self, parent=None):
        super(ViewPhotosPopup, self).__init__(parent)
        self.setWindowTitle('Autogram - Image Viewer')
        self.setMinimumWidth(700)
        self.setMinimumHeight(700)
        self.initUI()

    def create_photo_stream(self):
        for post in os.listdir(POSTS_DIR):
            post_path = os.path.normpath(f'{POSTS_DIR}/{post}')
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


class UploadPhotosPopup(QWidget):

    def __init__(self, parent=None):
        super(UploadPhotosPopup, self).__init__(parent)
        self.chosen_image = None
        self.chosen_description = None

        self.btn_ok = QPushButton("OK")
        self.btn_ok.setEnabled(False)
        self.chosen_image_label = QLabel('No image selected')
        self.description_textbox = QPlainTextEdit(QWidget().resize(150, 40))

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
            destination = os.path.normpath(f'{POSTS_DIR}/{file_name}')
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

        data = {
            'photo': self.chosen_image,
            'description': self.chosen_description
        }

        if os.path.exists(SCHEDULE):
            print('Editing existing schedule file')

            # Having issue doing this in one context as it was reading a stale version of the file
            # Therefore, read the file and get the data. Close the file.
            with open(SCHEDULE, 'r') as schedule_file:
                schedule = json.load(schedule_file)
                schedule.append({
                    'photo': self.chosen_image,
                    'description': self.chosen_description
                })
            # Then read the file again to write to it
            with open(SCHEDULE, 'w') as schedule_file:
                json.dump(schedule, schedule_file)
        else:
            print('Creating new schedule file!')
            with open(SCHEDULE, 'w') as schedule_file:
                json.dump([data], schedule_file)

    def close(self):
        self.chosen_description = None
        self.chosen_image = None
        self.chosen_image_label.setText('No image selected')
        self.description_textbox.clear()
        super().close()

    def open_file_dialog(self):
        return QFileDialog.getOpenFileName(self, 'Autogram', POSTS_DIR, 'All Files (*)')


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    autogram = AutogramApp()
    autogram.show()
    sys.exit(app.exec_())

