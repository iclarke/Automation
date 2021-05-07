from selenium import webdriver
import json
import os
import datetime as d
import shutil

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait


# Automation for Le Monde

# 1. Navigate to website and log in
lemonde_id = 'samy.doreau@gmail.com'
lemonde_pwd = 'A2O0I164ab@@'

home_page = 'https://journal.lemonde.fr/'


def move_files():
    dir_path = 'C:\\Users\\samy.doreau\\Downloads\\'
    target_path = 'C:\\Users\\samy.doreau\\Dropbox\\Code\\Automation\\output\\PDF_Lemonde\\'
    today = d.datetime.now().date()
    for file in os.listdir(dir_path):
        file_time = d.datetime.fromtimestamp(
            os.path.getctime(dir_path + file))
        filename, file_extension = os.path.splitext(f'{dir_path}{file}')
        if file_time.date() == today and file_extension == '.pdf':
            shutil.move(f'{dir_path}{file}', f'{target_path}{file}')


move_files()
