import json
with open('myproject/creat_music_data/main_config.json') as f:
        config = json.load(f)


print(config["relative"])