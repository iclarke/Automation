from lm_functions import *
clear_directory("output/PDF_Lemonde")
driver = init_driver()
lm_login(driver)
print_articles(driver, 100)
move_files()
