"""建立資料庫!!!!!"""
import re
# 自製
from file import File
from control import Controller

if __name__ == "__main__":
    file = File(test= True)
    while True:
        counters = 0
        max_counters = file.get_max_counters()
        params  , artsit_list = file.get_csv_data(processed_counters= counters)
        controller = Controller(artist_list= artsit_list , params= params)
        success = controller.run()
        if success: 
            if counters == max_counters:
                break
            counters +=1
        

    print("DONE!!!")
   


