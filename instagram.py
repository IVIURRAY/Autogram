import time
import autoit

from selenium import webdriver
from selenium.webdriver.chrome.options import *


class Autogram:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(executable_path='chromedriver/chromedriver.exe', options=self._get_options())

    @staticmethod
    def _get_options():
        options = Options()
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-logging")
        options.add_argument("--mute-audio")
        options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')

        return options

    def open_instagram(self):
        print('Opening Instagram...')
        self.driver.get("https://www.instagram.com/accounts/login/?hl=en")
        time.sleep(3)

    def login(self):
        print('Logging into Instagram...')
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div/div/div/form/div[4]/div/label/input').send_keys(self.username)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div/div/div/form/div[5]/div/label/input').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div/div/div/form/div[7]/button').click()

    def profile_page(self):
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[5]').click()
        time.sleep(0.5)

    def popup_close_save_login_info(self):
        print('Trying to close `save login info` popup...')
        attempts = 0
        while True:
            try:
                time.sleep(0.5)
                self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/section/div/button').click()
                break
            except:
                pass
                attempts += 1
                if attempts > 5:
                    print('Did not find `save login info` popup')
                    break

    def popup_close_turn_on_notifications(self):
        print('Trying to close `turn on notifications` popup...')
        attempts = 0
        while True:
            try:
                time.sleep(0.5)
                self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click()
                break
            except:
                pass
                attempts += 1
                if attempts > 5:
                    print('Did not find `turn on notifications` popup')
                    break

    def popup_close_add_to_home_screen(self):
        print('Trying to close `add to home screen` popup...')
        attempts = 0
        while True:
            try:
                time.sleep(0.5)
                self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click()
                break
            except:
                pass
                attempts += 1
                if attempts > 5:
                    print('Did not find `add to home screen` popup')
                    break

    def upload_image(self, file_path, description=''):
        # 1. Click upload image button
        print('Clicking `upload` button...')
        self.driver.find_element_by_xpath("//div[@role='menuitem']").click()
        time.sleep(2)

        # 2. Get the windows file explorer window that opened
        # Add the image path and click enter
        print('Uploading image to file explorer...')
        autoit.win_active("Open")
        autoit.control_send("Open", "Edit1", os.path.normpath(os.getcwd() + '/' + file_path))
        autoit.control_send("Open", "Edit1", "{ENTER}")
        time.sleep(2)

        # 3. Image should import and click Next button
        print('Image importing and processed to description...')
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/div[1]/header/div/div[2]/button').click()
        time.sleep(2)

        # 4. Add description
        print('Adding description...')
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/div[2]/section[1]/div[1]/textarea').click()
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/div[2]/section[1]/div[1]/textarea').send_keys(description)
        time.sleep(2)

        # 5. CLick Share
        print('Clicking `Share`!')
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/div[1]/header/div/div[2]/button').click()
        time.sleep(4)
        print('Upload completed.')


if __name__ == '__main__':
    ig = Autogram('<USERNAME>', '<PASSWORD>')
    ig.open_instagram()
    ig.login()
    ig.popup_close_save_login_info()
    ig.popup_close_turn_on_notifications()
    ig.popup_close_add_to_home_screen()

    description = 'Automatically upload this image using Code! \nSo I\'ve already got bored of positing to Instagram so I created a script to do it for me #automation #python \nGithub: https://github.com/IVIURRAY/Autogram'
    ig.upload_image('posts\image-sample-upload.jpg', description=description)
    ig.popup_close_turn_on_notifications()
    ig.profile_page()
