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


# Automation for Le Monde

# 1. Navigate to website and log in
lemonde_id = 'samy.doreau@gmail.com'
lemonde_pwd = 'A2O0I164ab@@'

home_page = 'https://journal.lemonde.fr/'


def scan_downloads_folder(dir_path):
    file_count = 0
    for file in os.listdir(dir_path):
        file_time = d.datetime.fromtimestamp(
            os.path.getctime(dir_path + '/' + file))
        filename, file_extension = os.path.splitext(f'{dir_path}/{file}')
        if file_time.date() == today and file_extension == '.pdf':
            file_count += 1

    return file_count


def move_files(dir_path, target_path):
    files_moved = 0
    today = d.datetime.now().date()
    for file in os.listdir(dir_path):
        file_time = d.datetime.fromtimestamp(
            os.path.getctime(dir_path + '/' + file))
        filename, file_extension = os.path.splitext(f'{dir_path}/{file}')
        if file_time.date() == today and file_extension == '.pdf':
            try:
                shutil.move(f'{dir_path}/{file}', f'{target_path}/{file}')
                files_moved += 1
                print(f'{files_moved} files moved', end='')

            except:
                print(f'Unable to move file {file}')
    return print(f'Moving complete, {files_moved} were moved to the target folder.')


def scan_directory(dir_name):
    file_count = 0
    for filename in os.listdir(dir_name):
        file_path = os.path.join(dir_name, filename)
        if os.path.isfile(file_path):
            file_count += 1
    return file_count


def ask_questions(answer_set, question_text):
    question_cleared = False

    while question_cleared == False:
        user_input = input(question_text)
        if user_input.lower() in answer_set:
            question_cleared = True
            return user_input


def clear_directory(dir_name):

    for filename in os.listdir(dir_name):
        file_path = os.path.join(dir_name, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"File {file_path} cleared")
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def init_driver():
    appState = {
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
    profile = {
        'printing.print_preview_sticky_settings.appState': json.dumps(appState),
        "directory_upgrade": True,
        "download.default_directory": "C:\\Users\\samy.doreau\\Dropbox\\Code\\Automation\\output\\PDF",
        "extensions_to_open": ""
    }

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', profile)
    chrome_options.add_argument('--kiosk-printing')

    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver


def lm_login(driver):

    # Navigate to home page and click "Lire"
    driver.get(
        'https://journal.lemonde.fr/')

    wait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '/html/body/div/div[7]/div[2]/div/div[1]/div[1]/div/div/div[4]/div'))).click()

    # Previous edition for testing

    # wait(driver, 10).until(EC.visibility_of_element_located(
    #     (By.XPATH, '/html/body/div/div[7]/div[2]/div/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]/div[1]/img'))).click()

    # Populate login form
    wait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '/html/body/div/main/section[3]/main/form/div[1]/input'))).send_keys(lemonde_id)
    wait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '/html/body/div/main/section[3]/main/form/div[2]/input'))).send_keys(lemonde_pwd)

    wait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '/html/body/div/main/section[3]/main/form/div[5]/button'))).click()


def print_articles(driver, nb_of_articles):
    articles_printed = 0
    # CLick on first article, then use arrows to iterate
    wait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '/html/body/div[2]/div[8]/div[2]/div[1]/div[1]/div[1]/div/div/div[3]/div/div[1]/div[1]/div/div[2]/div[2]'))).click()

    for i in range(nb_of_articles):
        try:
            print(f"Showing article {i}")
            wait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[2]/div[5]/div/div/div[3]/div[2]/div/div'))).click()

            # Print content
            driver.execute_script('window.print();')

            print(f'{articles_printed} articles printed.')

        except:
            print(f'Could not print article {i}')
            break
