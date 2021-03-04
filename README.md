# Red to You
RedToYou is a python based progrma that aims to convert reddit threads to interative videos suitable forpersonal viewing or alternativly uploading to YouTube (hence the name Red(dit)ToYou(tube))
# Setup
Before running the program, it is required that the user installs python as well as pip (pythons package manager)
after installing python and pip you will need to install the following python librarys
praw (library for inseracting with reddit's APi)
PIL (library ffor image creation)
time
datetime
shutil (for file deletion)
re
glob (to import files mathing a specific pattern)
random
threading (for multi threading)
timeit (AI is used to calulated the length of time it will take to render the video based on number gathered from this library)
json
csv (AI is fed a CSV)
pandas (Used in AI)
sklearn (AI Engine)
mp3_tagger (Gets information from the mps files in the mp3 folder
itertools
# Using the Program
Upon lanching the program th used will be asked whether they would like have thier video created using the classic version of reddit or the redesigned version of reddit 

Simply type 1 or 0 for your prefered mode

Next the the user will be asked if they would like to run the progrma in single threaded or multithreaded mode.
It is recommended that users with ram ammounts below 16GB run the program in single threaded mode to minimize the number of objects in memeory

After, the user will be prompted to enter and upper bound for thier desired video length (the ai will run until it finds which posts to include to get a time in the acceptable range. It is recommended that the user enter a number roughly 30 secs higher than the time they deisire
The next option, backgrounds color, is only applicappple to users who plan on uploading thier video to the web. The prompt asks the user what color backgorund they would like thier youtube thumbnail, to be.

Next the user is prompted for a title they would like for thier thumbnail, this is only needed when the title of the post exceeds 100 characters causing the text to drop off the image
