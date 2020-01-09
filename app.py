import os
from PyQt5.QtWidgets import *


class AutogramApp(QDialog):

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
            files, _ = self.open_file_dialog()
            print(files)

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
        return QFileDialog.getOpenFileNames(self, 'Chose Autogram Upload', 'posts', 'All Files (*)')

    def scheduler_section(self):
        box = QGroupBox("Scheduler")

        layout = QVBoxLayout()
        layout.addWidget(QPushButton('Upload'))
        layout.addWidget(QPushButton('View'))
        box.setLayout(layout)

        return box


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    autogram = AutogramApp()
    autogram.show()
    sys.exit(app.exec_())

