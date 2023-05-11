"""建立資料庫!!!!!"""
import re
# 自製
from file import File
from control import Controller

if __name__ == "__main__":
    file = File(test= True)
    counters = 0
    max_counters = file.get_max_counters()
    while True:
        params  , artsit_list = file.get_csv_data(processed_counters= counters)
        controller = Controller(artist_list= artsit_list , params= params)
        success = controller.run()
        if success: 
            counters +=1
            if counters == max_counters:
                break
            print(f"next file on {file.get_now_processed_file_path()}")

    print("DONE!!!")
   


