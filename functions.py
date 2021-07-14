
import datetime as d
import os
import shutil
import json
from selenium import webdriver
import pandas as pd
import xml.etree.cElementTree as et
from pathlib import Path
# from webdriver_manager.chrome import ChromeDriverManager
from pysitemap import crawler
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait


def clear_directory(dir_name):

    for filename in os.listdir(dir_name):
        file_path = os.path.join(dir_name, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"File {file_path} cleared")
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def generate_site_maps(end_date, section_list):

    exclusion_list = [d.strftime('%Y/%m/%d')
                      for d in pd.date_range('19500101', end_date)]
    exclusion_list.extend(['?page', ';var'])

    for s in section_list:
        root_url = f"https://www.economist.com/{s}"
        print(f"Processing section : {s} | URL = {root_url}")
        crawler(
            root_url, out_file=f"./output/sitemap_{s}.xml", exclude_urls=exclusion_list)

    return('Site maps generated and saved to the output folder')


def generate_url_list(section_list):

    # Initialise data frame
    url_df = pd.DataFrame(columns=['section', 'url'])
    df_index = 0

    for s in section_list:
        section_url_df = pd.DataFrame(columns=['section', 'url'])
        xtree = et.parse(f"output/sitemap_{s}.xml")
        root_node = xtree.getroot()

        # Define minimum URL length to filer out incorrect URLs
        min_string = f"https://www.economist.com/{s}"
        min_length = len(min_string) + 1
        # print(f"The minimum length is {min_length}")

        for url in root_node.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc = url.find(
                '{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
            section_url_df.loc[df_index] = [f"{s}", loc]
            df_index += 1

        section_url_df = section_url_df[section_url_df['url'].map(
            len) > min_length]
        url_df = pd.concat([url_df, section_url_df])

        print(f"Section {s} - completed")

    return url_df['url'].tolist()


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
    download_dir = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), r"output\PDF\"")
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


def login(driver):
    id = "s.amydoreau@gmail.com"
    pwd = "A2O0I164AB@@"

    # Navigate to home page, dismiss banners & login

    driver.get(
        'https://www.economist.com/')
    print('Dimissing cookie banner')
    driver.find_element_by_xpath(
        '//*[@id="_evidon-banner-acceptbutton"]').click()
    driver.execute_script("window.scrollTo(0, 50)")
    # print('Dimissing sub banner')
    # driver.find_element_by_xpath(
    #     '/html/body/div[1]/div/div[2]/div/button').click()

    wait(driver, 10).until(EC.visibility_of_element_located(
        (By.LINK_TEXT, "Sign in"))).click()

    # find username/email field and send the username itself to the input field
    driver.find_element_by_id("email").send_keys(id)

    # click continue button
    driver.find_element_by_xpath(
        '//*[@id="__next"]/div/main/div/div/form/button').click()

    # find password input field and insert password as well

    wait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '/html/body/div[3]/div[3]/div[1]/div/div/div/div[2]/div/div/c-lwc-login-form/lightning-card/article/div[2]/slot/div[1]/div[2]/div/lightning-input/div[1]/input'))).send_keys(pwd)

    print("Password input successful")
    # click login button
    wait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '/html/body/div[3]/div[3]/div[1]/div/div/div/div[2]/div/div/c-lwc-login-form/lightning-card/article/div[2]/slot/div[1]/div[3]/div[2]/lightning-button/button'))).click()
    print("Login form submitted")


def print_page(driver, page_url):

    # Navigate to desired page and print to PDF
    driver.get(page_url)
    driver.execute_script('window.print();')


def move_files():
    # dir_path = 'C:\\Users\\samy.doreau\\Downloads\\'
    # target_path = 'C:\\Users\\samy.doreau\\Dropbox\\Code\\Automation\\output\\PDF\\'
    dir_path = str(Path.home() / "Downloads")
    target_path = f'{Path.home()}/Dropbox/Code/Automation/output/PDF_Economist'
    files_moved = 0

    today = d.datetime.now().date()
    for file in os.listdir(dir_path):
        file_time = d.datetime.fromtimestamp(
            os.path.getctime(dir_path + '/' + file))
        filename, file_extension = os.path.splitext(f'{dir_path}/{file}')
        if file_time.date() == today and file_extension == '.pdf':
            shutil.move(f'{dir_path}/{file}', f'{target_path}/{file}')
            files_moved += 1

    print(f'********* {files_moved} files moved *************')
