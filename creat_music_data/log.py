import os
import logging


def log(path: str, success: bool):
    log_dir = './log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, 'creat_data.log')
    # print(log_file_path)
    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[file_handler])

    if success:
        logging.info(f"Downloaded folder {path}")
    elif success is False:
        logging.error(f"Downloaded folder {path}")
    elif success is None:
        logging.warning(f"Downloaded folder {path}")
