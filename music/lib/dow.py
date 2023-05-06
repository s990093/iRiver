"""直接使用  不須額外"""
import threading
import os 
import logging
# 自製
import music.lib.download.img as img
import music.lib.download.y2mate as y2mate


#         log(music_ID= music_ID , artist=artist, success=res)

def download(music_ID_list: list , 
             img_url: str , 
             cover_img_url: str , 
             artist_img_url: str,
             artsit: str) -> list:
    """input music_ID_list
        output music_ID_list of res    
    """
    class WorkerThread(threading.Thread):
        def __init__(self, music_ID ,artist):
            super().__init__()
            self.music_ID = music_ID
            self.artist = artist
            self.result = None

        def run(self):
            self.result = y2mate.download_audio(
                music_ID=self.music_ID, artist=self.artist)
            log(music_ID= music_ID, artist=self.artist , success= self.result)
            # img
            img.download_img(url= img_url ,
                             file_name= f"{music_ID}.jpg" ,
                             file_dir= f"media/{artsit}/img/")

            # cover
            img.download_img_base64(url= cover_img_url ,
                                    file_name='cover.jpg' ,
                                    file_dir= f"media/{artsit}/img/" )
            
            # artist
            img.download_img(url= artist_img_url ,
                             file_name='artist.jpg' ,
                             file_dir= f"media/{artsit}/img/")

   
    threads = []
    for music_ID in music_ID_list:
        t = WorkerThread(music_ID= music_ID , artist= artsit)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    
    return True





def log(music_ID, artist, success):
    log_dir = './log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, 'dow_song.log')
    print(log_file_path)
    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[file_handler])

    if success:
        logging.info(f"Downloaded music '{music_ID}' by '{artist}' successfully.")
    elif success is False:  
        logging.error(f"Failed to download music '{music_ID}' by '{artist}'.")
    elif success is None:
        logging.warning(f"Already exists '{music_ID}' by '{artist}'.")
