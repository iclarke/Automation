from lm_functions import *
NEWS_FR_DIR = 'output/PDF_Lemonde'
DOWNLOADS_FOLDER_PATH = str(Path.home() / "Downloads")
TARGET_PDF_FOLDER_PATH = f'{Path.home()}/Dropbox/Code/Automation/output/PDF_Lemonde'
# exit_process = False

# while exit_process == False:

#     # Clear directory with previous downloads

#     files_to_clear = scan_directory(dir_name=NEWS_FR_DIR)
#     if files_to_clear > 0:
#         input_clear_files_prompt = f"{files_to_clear} files found, proceed and remove ? (Y/N)"
#         clear_files_user_selection = ask_questions(
#             ['y', 'n'], input_clear_files_prompt)
#         if clear_files_user_selection == 'n':
#             exit_process = True
#         else:
#             clear_directory("output/PDF_Lemonde")
#     driver = init_driver()
#     try:
#         lm_login(driver)
#     except:
#         print('Unable to log in.')
#     print_articles(driver, 100)

# Scan downloads path
# downloads_found = scan_downloads_folder(dir_path=DOWNLOADS_FOLDER_PATH)
# print(f" --> {downloads_found} files downloaded from the website")

move_files(dir_path=DOWNLOADS_FOLDER_PATH,
           target_path=TARGET_PDF_FOLDER_PATH)

# Move file to rm2

import remarkable_fs
