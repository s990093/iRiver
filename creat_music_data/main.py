"""建立資料庫!!!!!"""
import re
# 自製
from file import File
import file
from control import Controller
from log import log
   
def run(folder :str , directory :str):
     while True:
        file = File(folder= folder , directory = directory)
        counters = 0
        max_counters = file.get_max_counters()
        params  , artsit_list = file.get_csv_data(processed_counters= counters)
        controller = Controller(artist_list= artsit_list , params= params)
        success = controller.run()
        if success: 
            counters +=1
            if counters == max_counters:
                return True
            print(f"next file on {file.get_now_processed_file_path()}")


if __name__ == "__main__":
    folders = file.get_all_folder(directory= "test")
    for folder in folders:
        success = run(folder= folder , directory= "test")
        log(path= f"{folder}" , success= success)
    print("DONE!!!")