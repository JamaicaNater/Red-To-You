# Red to You
RedToYou is a python-based program that aims to convert reddit threads to interactive videos suitable for personal viewing or alternatively uploading to YouTube (hence the name Red(dit)ToYou(tube))
# Setup
Before running the program, it is required that the user installs python as well as pip (pythons package manager)

After installing python and pip you will need to install the following python libraries:

praw (library for interacting with reddit's API)

PIL (library for image creation)

time

datetime

shutil (for file deletion)

re

glob (to import files matching a specific pattern)

random

threading (for multi-threading)

timeit (AI is used to calculate the length of time it will take to render the video based on number gathered from this library)

json

csv (AI is fed a CSV)

pandas (Used in AI)

sklearn (AI Engine)

mp3_tagger (Gets information from the mp3 files in the mp3 folder

itertools

In addition, you will need to provide your own NewError.mp4 (transiton) and outro.mp4 (video outro) in the Static folder as well as populate your own tagged music (mp3) in Static/DynamicMusic

# Using the Program
Upon launching the program, the user will be asked whether they would like to have their video created using the classic version of reddit or the redesigned version of reddit 

Simply type 1 or 0 for your preferred mode

Next the user will be asked if they would like to run the program in single threaded or multithreaded mode.
It is recommended that users with ram amounts below 16GB run the program in single threaded mode to minimize the number of objects in memory

After, the user will be prompted to enter and upper bound for their desired video length (the ai will run until it finds which posts to include to get a time in the acceptable range. It is recommended that the user enter a number roughly 30 secs higher than the time they desire
The next option, backgrounds color, is only applicable to users who plan on uploading their video to the web. The prompt asks the user what color background they would like their YouTube thumbnail, to be.

Next the user is prompted for a title they would like for their thumbnail, this is only needed when the title of the post exceeds 100 characters causing the text to drop off the image

![image](https://user-images.githubusercontent.com/52978102/110018083-8e82e080-7cec-11eb-9271-f6a2947c119d.png)
# What is Happening ?
The program first starts by gathering data from the reddit link that the user has inserted. Then the program calculates the length in time that it estimates the Text to Speech API will take to read text file based on the sklearn python prediction library. A loop is then created and is run until the program finds a satisfactory time for the program.
One this step is done; the program creates temporary files used in the creation of the video file. The program also cleans up the previous folder in the case that the program didn’t exit successfully the first time.

![image](https://user-images.githubusercontent.com/52978102/110021874-e7547800-7cf0-11eb-8298-b9d3c16782dd.png)

 
After that, the user is informed what the maximum length of the video would be if the user had not limited to program to what they passed to the program. 

![image](https://user-images.githubusercontent.com/52978102/110021882-ec192c00-7cf0-11eb-9e96-664e2395adba.png)
 
Next the AI engine runs and calculates how long it would take the Text to speech engine to read the saved text files 

![image](https://user-images.githubusercontent.com/52978102/110021909-f3403a00-7cf0-11eb-8b75-0ae2e2877792.png)
 
Next the  program show the user the estimated video length as well as how many reddit comments the video will include
>threshold : threshold multiplied by the upvote value of the parent comment gives the minimum value a reply needs to be included in the video

![image](https://user-images.githubusercontent.com/52978102/110021933-fc310b80-7cf0-11eb-8518-983d5fadee52.png)
 
The program also gives the user feedback as the program progresses
	If the user uses multithreaded processes these number will be out of order however shorter comments will appear first in the video
	If the user uses single threaded, comments will match the order they appear in the thread
	In both cases, however the program scrambles the order in with the comments appear
Because video and audio as computed separate, we can give the user that actual video length quickly, before the video begins to render, this give the user to option to quit the program and enter an alternate value before waited for the file to render.

![image](https://user-images.githubusercontent.com/52978102/110022026-12d76280-7cf1-11eb-8437-090a3aa0ae7d.png)

After, the video is built using the images created from the PIL Library as well as the audio from the TTS library.

![image](https://user-images.githubusercontent.com/52978102/110022056-19fe7080-7cf1-11eb-8ac5-b574c5d2ef7e.png)
 
Then the program finishes running

![image](https://user-images.githubusercontent.com/52978102/110022082-1ff45180-7cf1-11eb-8c61-164946bc1d9a.png)

After Navigating to Subs/Vid we see the following:

![image](https://user-images.githubusercontent.com/52978102/110022120-297db980-7cf1-11eb-81c2-ecbbdaec3a00.png)

The video file is saved as the video’s unique identifier

# Additional Information 
After the program runs, diagnostic information such as the total number of characters in the program as well as the programs duration are saved into a csv file which we feed into our learning tool, thus the program gets better and predicting video length over time

![image](https://user-images.githubusercontent.com/52978102/110022300-5cc04880-7cf1-11eb-876f-9c0a61cf76ab.png)
 
Because the program is built to be used by youtubers, the program also generates a description file with can the easily copied into YouTube

![image](https://user-images.githubusercontent.com/52978102/110023751-2388d800-7cf3-11eb-9e83-b25024151b13.png)

The program as present relies on a windows-only command line utility called Balcon meaning there is no Linux support planned.
# Beta 
Currently I am working on a system that runs in an infinite loop that uploads video at set intervals throughout the day with no user input, a fully automated YouTube Channel, stay tuned.

