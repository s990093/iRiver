import os


directory = "artist"

# get a list of all directories in the specified directory
folders = [f for f in os.listdir(
    directory) if os.path.isdir(os.path.join(directory, f))]

