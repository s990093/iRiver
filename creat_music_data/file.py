import os
import glob
import csv


class File:
    def __init__(self):
        super().__init__()
        self.csv_files = []
        self.processed_counters = 0
    
    def get_now_rocessed_counters(self):
        return self.processed_counters

    def get_all_file_names(self):
        for file_path in glob.glob(os.path.join('artist', '*.csv')):
            self.csv_files.append(file_path)
        print(self.csv_files)

    def get_csv_data(self, processed_counters=0):
        self.processed_counters = processed_counters
        with open(self.csv_files[self.processed_counters], newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            header = next(reader)
            params = {
                'sources':  header[0],
                'style':  header[1],
                'country':  header[2],
                'language':  header[3],
            }
            count = 0
            artist = []

            for col in reader:
                for row in col:
                    artist.append(row.split())

            return params, artist
