"""建立資料庫!!!!!"""
import json
# 自製
from file import File
import file
from control import Controller
from log import log
   
def run(folder :str , config):
     while True:
        file = File(folder= folder , directory = config["directory"])
        counters = 0
        max_counters = file.get_max_counters()
        params  , artsit_list = file.get_csv_data(processed_counters= counters)
        controller = Controller(artist_list= artsit_list , params= params ,  
                                max_thread= config["max_thread"], max_dow_thread= config["max_dow_thread"])
        success = controller.run()
        if success: 
            counters +=1
            if counters == max_counters:
                return True
            print(f"next file on {file.get_now_processed_file_path()}")


if __name__ == "__main__":
    with open('main_config.json') as f:
        config = json.load(f)
    folders = file.get_all_folder(directory=  config["directory"])
    for folder in folders:
        success = run(folder= folder , config= config)
        log(path= f"{folder}" , success= success)
    print("DONE!!!")