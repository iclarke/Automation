from selenium import webdriver
import json
import os
import datetime as d
from pathlib import Path
import shutil

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait

LEMONDE_ID = 'samy.doreau@gmail.com'
LEMONDE_PWD = 'A2O0I164ab@@'
LEMONDE_HOME_PAGE_URL = 'https://journal.lemonde.fr/'
NEWS_FR_DIR = 'output/PDF_Lemonde'
DOWNLOADS_FOLDER_PATH = str(Path.home() / "Downloads")
TARGET_PDF_FOLDER_PATH = f'{Path.home()}/Dropbox/Code/Automation/output/PDF_Lemonde'
LEMONDE_HOME_PAGE_URL = 'https://journal.lemonde.fr/'
COOKIE_BANNER_XPATH = '/html/body/div[2]/div/footer/button[1]'
LOGIN_FORM_ID_XPATH = '/html/body/div/main/section[3]/main/form/div[1]/input'
LOGIN_FORM_PWD_XPATH = '/html/body/div/main/section[3]/main/form/div[2]/input'
LOGIN_FORM_SUBMIT_XPATH = '/html/body/div/main/section[3]/main/form/div[5]/button'
FIRST_ARTICLE_BUTTON_XPATH = '/html/body/div[2]/div[9]/div[2]/div[1]/div[1]/div[1]/div/div/div[3]/div/div[1]/div[1]/div/div[2]/div[5]'
NEXT_ARTICLE_BUTTON_XPATH = '/html/body/div[2]/div[6]/div/div/div[3]/div[2]/div'
LIRE_BUTTON_XPATH = '/html/body/div/div[7]/div[2]/div/div[1]/div[1]/div/div/div[4]/div/div'
APP_STATE = {
    "recentDestinations": [
        {
            "id": "Save as PDF",
            "origin": "local",
            "account": ""
        }
    ],
    "selectedDestinationId": "Save as PDF",
    "version": 2
}
PROFILE = {
    'printing.print_preview_sticky_settings.appState': json.dumps(APP_STATE),
    "directory_upgrade": True,
    "download.default_directory": "C:\\Users\\samy.doreau\\Dropbox\\Code\\Automation\\output\\PDF",
    "extensions_to_open": ""
}


class LeMondeCrawler:
    def __init__(self):

        self.today = d.datetime.now().date()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', PROFILE)
        chrome_options.add_argument('--kiosk-printing')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.max_articles = 100
        # print('Driver successfully initialised')

    def scan_downloads_folder(self):
        file_count = 0
        for file in os.listdir(DOWNLOADS_FOLDER_PATH):
            file_time = d.datetime.fromtimestamp(
                os.path.getctime(DOWNLOADS_FOLDER_PATH + '/' + file))
            filename, file_extension = os.path.splitext(
                f'{DOWNLOADS_FOLDER_PATH}/{file}')
            if file_time.date() == self.today and file_extension == '.pdf':
                file_count += 1

        return file_count

    def move_files(self):
        files_moved = 0
        today = d.datetime.now().date()
        for file in os.listdir(DOWNLOADS_FOLDER_PATH):
            file_time = d.datetime.fromtimestamp(
                os.path.getctime(DOWNLOADS_FOLDER_PATH + '/' + file))
            filename, file_extension = os.path.splitext(
                f'{DOWNLOADS_FOLDER_PATH}/{file}')
            if file_time.date() == today and file_extension == '.pdf':
                try:
                    shutil.move(f'{DOWNLOADS_FOLDER_PATH}/{file}',
                                f'{TARGET_PDF_FOLDER_PATH}/{file}')
                    files_moved += 1
                    print(f'{files_moved} files moved', end='')

                except:
                    print(f'Unable to move file {file}')
        return print(f'Moving complete, {files_moved} were moved to the target folder.')

    def scan_directory(self):
        file_count = 0
        for filename in os.listdir(DOWNLOADS_FOLDER_PATH):
            file_path = os.path.join(DOWNLOADS_FOLDER_PATH, filename)
            if os.path.isfile(file_path):
                file_count += 1
        return file_count

    def clear_directory(self):

        for filename in os.listdir(DOWNLOADS_FOLDER_PATH):
            file_path = os.path.join(DOWNLOADS_FOLDER_PATH, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f"File {file_path} cleared")
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def lm_login(self):

        # Navigate to home page and click "Lire"
        print(f'Navigating to home page URL : {LEMONDE_HOME_PAGE_URL}')
        self.driver.get(LEMONDE_HOME_PAGE_URL)

        # Clear cookie banner
        try:
            wait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, COOKIE_BANNER_XPATH))).click()
        except:
            print('No cookie banner found')

        wait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, LIRE_BUTTON_XPATH))).click()

        # Populate login form
        wait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, LOGIN_FORM_ID_XPATH))).send_keys(LEMONDE_ID)
        wait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, LOGIN_FORM_PWD_XPATH))).send_keys(LEMONDE_PWD)

        wait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, LOGIN_FORM_SUBMIT_XPATH))).click()

    def print_articles(self):
        articles_printed = 0
        # CLick on first article, then use arrows to iterate

        wait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, FIRST_ARTICLE_BUTTON_XPATH))).click()

        for i in range(self.max_articles):
            try:

                wait(self.driver, 30).until(EC.visibility_of_element_located(
                    (By.XPATH, NEXT_ARTICLE_BUTTON_XPATH))).click()

                # Print content
                self.driver.execute_script('window.print();')

                print(f'{articles_printed} articles printed.')

            except:
                print(f'Could not print article {i}')
                break
