import os
import datetime as d
import shutil
from pathlib import Path

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
