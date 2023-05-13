import json
import os

# 获取根目录路径
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 使用绝对导入
from myproject.creat_music_data.lib.file import File
import myproject.creat_music_data.lib.file as file
from myproject.creat_music_data.lib.control import Controller
import myproject.creat_music_data.lib.log as log
