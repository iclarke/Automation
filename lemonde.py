from lm_crawler import *

lemonde_daily_crawler = LeMondeCrawler()

files_to_clear = lemonde_daily_crawler.scan_directory()
if files_to_clear > 0:
    lemonde_daily_crawler.clear_directory()
    print(f'{files_to_clear} files deleted')
else:
    print('No files to clear')
lemonde_daily_crawler.lm_login()


lemonde_daily_crawler.print_articles()
# Scan downloads path
downloads_found = lemonde_daily_crawler.scan_downloads_folder()
print(f" --> {downloads_found} files downloaded from the website")

lemonde_daily_crawler.move_files()
