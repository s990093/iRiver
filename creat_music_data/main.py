"""建立資料庫!!!!!"""
import re
# 自製
from lib.web_scutter.youtube import query_youtube
from file import File

if __name__ == "__main__":
    file = File()
    file_csv = file.get_all_file_names()
    rocessed_counters = file.get_now_rocessed_counters()
    while True:
        params  , artsit = file.get_csv_data(file.get_now_rocessed_counters())

   


