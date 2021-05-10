import shutil
import os
import datetime as d
from pathlib import Path


dir_path = str(Path.home() / "Downloads")
target_path = f'{Path.home()}/Dropbox/Code/Automation/output/PDF_Lemonde'

today = d.datetime.now().date()
for file in os.listdir(dir_path):
    file_time = d.datetime.fromtimestamp(
        os.path.getctime(dir_path + '/' + file))
    filename, file_extension = os.path.splitext(f'{dir_path}/{file}')
    if file_time.date() == today and file_extension == '.pdf':
        print(filename)
        shutil.move(f'{dir_path}/{file}', f'{target_path}/{file}')
