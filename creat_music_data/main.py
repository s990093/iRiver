"""建立資料庫!!!!!"""
import csv
import re
# 自製
from lib.web_scutter.youtube import query_youtube

if __name__ == "__main__":
    with open('artist/test.csv', newline='' , encoding= 'utf-8') as csvfile:
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
    print(artist[0])


