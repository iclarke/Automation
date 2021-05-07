from functions import generate_site_maps, generate_url_list, print_to_pdf, clear_directory, login, print_page, init_driver, move_files

section_list = ['leaders', 'britain', 'europe', 'united-states', 'middle-east-and-africa', 'briefing',
                'the-americas', 'asia', 'china', 'international', 'business', 'finance-and-economics', 'science-and-technology', 'books-and-arts', 'business', 'obituary']


clear_directory("output")
clear_directory("output/PDF")
#end_date = input("Enter end date as a string (YYYYMMDD) \n")
end_date = '20210507'
generate_site_maps(end_date, section_list)
url_list = generate_url_list(section_list)


driver = init_driver()
login(driver)
for url in url_list:
    print_page(driver, url)

move_files()
