"""建立資料庫!!!!!"""
import json

# 自製
from lib.file import File
import lib.file as file
from lib.control import Controller
import lib.log as log


def run(folder: str, config):
    while True:
        file = File(folder=folder, directory=config["directory"])
        counters = 0
        max_counters = file.get_max_counters()
        params, artsit_list = file.get_csv_data(processed_counters=counters)
        controller = Controller(artist_list=artsit_list, params=params,
                                max_thread=config["max_thread"], max_dow_thread=config["max_dow_thread"],
                                max_retries=config["max_retries"], relative=config["relative"])
        success = controller.run()
        if success:
            counters += 1
            if counters == max_counters:
                return True
            print(f"next file on {file.get_now_processed_file_path()}")


if __name__ == "__main__":
    with open('main_config.json') as f:
        config = json.load(f)

    last_process_folders = log.get_last_n_process_folders(20)
    folders = file.get_all_folder(directory=config["directory"])
    for folder in folders:
        if folder in last_process_folders:
            print(f"{folder} has already been processed, skipping...")
            continue
        log.wrtie(path=f"{folder}", success=run(folder=folder, config=config))

    print("DONE!!!")
