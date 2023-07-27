import RedditItem
import directories
from formatting import ui
from formatting import text_format
from formatting import utils

import praw
from moviepy.editor import *
from PIL import Image, ImageFont, ImageDraw
import textwrap
import time
import datetime
import shutil
import re
import glob
import os
from random import shuffle
import threading
import timeit
import json
import csv
import pandas as pd
from praw.models import Submission
from sklearn import linear_model
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
import moviepy
import logging
from dotenv import load_dotenv

"""
Word                    Definition
rtr                     Reply to a reply
threshold               Factor of the minimum score criteria of a comment eg. by default, if a comment
                        fails to receive 30% of the score of its parent, the comment is not included
balcon                  Text To Speech Command Line Utility
"""

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()
debug = True

# User Input
if (debug):
    mode = 0
    speed = 0
    reddit_link = "https://www.reddit.com/r/AskReddit/comments/wo4vb8/whats_something_that_people_turn_into_their_whole/"
    desired_vid_len = 99
    bgrd_choice = 0
    cust_title = '0'
else:
    mode = int(input('Mode; 0 = Redesign, 1 = Classic '))
    speed = int(input('\nSpeed; 0 = Multithreaded, 1 = Normal '))
    reddit_link = input('\nLink; Paste your desired reddit post:\n')
    desired_vid_len = int(input('\nTime; Enter your maximum desired video length (seconds): '))
    bgrd_choice = int(input('\nColor; Type your ui.BACKGROUND color option [0 = Transparent, 1 = Default, 2 = Black]: '))
    cust_title = input('\nTitle; Type a custom title for thumbnails, to  use default type 0\n')

# Reddit Setup
reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET'),
                     user_agent='Red-To-You')
submission: Submission = reddit.submission(url=reddit_link)

reddit_post = RedditItem.RedditItem(submission)
ui.init(mode, reddit_post.num_com)

number_comments = 25  # int(input('Type a Number Between 1 and 25 to represent the Number of Comments\n'))
threshold = .3  # float(input('Type a number between 0 and 1 to represent the reply threshold (.33 recommended) \n'))
MIN_SCORE = 50
DNE = 'Does Not Exist'



# EXE Directories
BALCON_DIR = os.path.dirname(os.path.abspath("balcon.exe"))
UPLOAD_DIR = os.path.dirname(os.path.abspath('Upload/youtubeuploader_windows_amd64.exe')) + '\\'

cWidth = 175    # Width between comments
rWidth = 168    # Width between replies
rtrWidth = 161  # Width between replies to replies
VID_FPS = 15    # Video frames per second

# Imported with moviepy
TRANSITION = VideoFileClip(f'{directories.CLIPS_DIR}/Transition.mp4').set_duration(.7).set_fps(VID_FPS)
OUTRO = VideoFileClip(f'{directories.CLIPS_DIR}/Outro.mp4').set_fps(VID_FPS)
SILENCE = AudioFileClip(f'{directories.AUDIO_DIR}Silence.wav').set_duration(.33)

def draw_outlined_text(x, y, draw, font, text, width=1, outline='black', fill='white'):
    """
    Function:   draw_outlined_text
    Definition: This function draws text on screen by superimposing 4 lawyers of the text at an outline distance apart
                then the function draws the fill text.
    Parameter:  x, y, draw (PIL method corresponding to a given image), text, width, outline
    Return:     NONE
    """
    draw.text((x - width, y - width), text, font=font, fill=outline)
    draw.text((x + width, y - width), text, font=font, fill=outline)
    draw.text((x - width, y + width), text, font=font, fill=outline)
    draw.text((x + width, y + width), text, font=font, fill=outline)

    # now draw the text over it
    draw.text((x, y), text, font=font, fill=fill)

def use_comment(comment):
    """
    Function:   use_comment
    Definition: This function determines whether or not we will use a comment in our program.
                we make this determination by checking if a comment was flagged with DNE upon initialisation; we also
                check to see if the comment meets the minimum score criteria.
    Parameter:  Reddit_Item
    Return:     boolean
    """
    index = str_comment_list.index(comment)
    if (comment_list[index].body != DNE) and (comment_list[index].score >= MIN_SCORE):
        if index == 0:
            return not submission.comments[0].stickied
        else:
            return True
    else:
        return False


def use_reply(comment):
    """
    Function:   use_reply
    Definition: This function determines whether or not we will use a reply in our program.
                we make this determination by checking if a reply was flagged with DNE upon initialisation; we also
                check to see if the comment meets the minimum score criteria.
                This is determined by checking if the score multiplied by the threshold is greater than or equal to
                the original comment
    Parameter:  Reddit_Item
    Return:     boolean
    """
    index = str_comment_list.index(comment)
    if (reply_list[index].body != DNE) and (reply_list[index].score >= threshold * comment_list[index].score):
        return True
    else:
        return False


def use_rtr(comment):
    """
    Function:   use_rtr
    Definition: This function determines whether or not we will use a reply in our program.
                First, we check if we even used a reply, then we check if a rtr was flagged with DNE upon
                initialisation; we also check to see if the comment meets the minimum score criteria.
                This is determined by checking if the score multiplied by the threshold is greater than or equal to
                the original comment.
    Parameter:  Reddit_Item
    Return:     boolean
    """
    index = str_comment_list.index(comment)
    if use_reply(comment) and (rtr_list[index].body != DNE) and (
            rtr_list[index].score >= reply_list[index].score * threshold):
        return True
    else:
        return False


def populate_lists():
    """
    Function:   populate_lists
    Definition: This function pulls all the relevant data from Reddit and loads it into memory.
                The function also formats the text.
    Parameter:  NONE
    Return:     NONE
    """
    for i in range(number_comments):  # gets all all comments saves them to a string
        # Creates the comments if they exist
        try:
            temp_com = utils.replace_me(submission.comments[i].body, all_rep, all_rep_with)
            temp_com = re.sub(r"\[(.+)\]\(.+\)", r"\1", temp_com)
        except:
            temp_com = DNE

        # Creates the authors if they exist
        if submission.comments[i].stickied:
            temp_com = DNE
        if temp_com != DNE:
            try:
                temp_name = submission.comments[i].author.name  # and indexes them starting at 0
            except AttributeError:
                temp_name = '[deleted]'

            temp_score = submission.comments[i].score
            temp_time = text_format.human_time(datetime.datetime.fromtimestamp(submission.comments[i].created))
            temp_gildings = submission.comments[i].gildings
        else:
            temp_name = DNE
            temp_score = DNE
            temp_time = DNE
            temp_gildings = DNE

        comment_list.append(RedditItem.RedditItem(temp_com, temp_name, temp_score, temp_time, temp_gildings))
        str_comment_list.append(comment_list[i].body)
        # logging.info(temp_gildings)
        del temp_com
        del temp_name
        del temp_score
        del temp_time
        del temp_gildings

    for i in range(number_comments):  # gets all all comments saves them to a string

        # Creates the comments if they exist
        try:
            temp_com = utils.replace_me(submission.comments[i].replies[0].body, all_rep, all_rep_with)
            temp_com = re.sub(r"\[(.+)\]\(.+\)", r"\1", temp_com)
        except:
            temp_com = DNE

        # Creates the authors if they exist
        if temp_com != DNE:
            try:
                temp_name = submission.comments[i].replies[0].author.name  # and indexes them starting at 0
            except AttributeError:
                temp_name = '[deleted]'
            temp_score = submission.comments[i].replies[0].score
            temp_time = text_format.human_time(datetime.datetime.fromtimestamp(submission.comments[i].replies[0].created))
            temp_gildings = submission.comments[i].replies[0].gildings

        else:
            temp_name = DNE
            temp_score = DNE
            temp_time = DNE
            temp_gildings = DNE

        reply_list.append(RedditItem.RedditItem(temp_com, temp_name, temp_score, temp_time, temp_gildings))

        del temp_com
        del temp_name
        del temp_score
        del temp_time
        del temp_gildings

    for i in range(number_comments):  # gets all all comments saves them to a string

        # Creates the comments if they exist
        try:
            temp_com = utils.replace_me(submission.comments[i].replies[0].replies[0].body, all_rep, all_rep_with)
            temp_com = re.sub(r"\[(.+)\]\(.+\)", r"\1", temp_com)
        except:
            temp_com = DNE

        # Creates the authors if they exist and indexes them starting at 0
        if temp_com != DNE:
            try:
                temp_name = submission.comments[i].replies[0].replies[0].author.name
            except AttributeError:
                temp_name = '[deleted]'
            temp_score = submission.comments[i].replies[0].replies[0].score
            temp_time = text_format.human_time(
                datetime.datetime.fromtimestamp(submission.comments[i].replies[0].replies[0].created))
            temp_gildings = submission.comments[i].replies[0].replies[0].gildings
        else:
            temp_name = DNE
            temp_score = DNE
            temp_time = DNE
            temp_gildings = DNE

        rtr_list.append(RedditItem.RedditItem(temp_com, temp_name, temp_score, temp_time, temp_gildings))

        del temp_com
        del temp_name
        del temp_score
        del temp_time
        del temp_gildings


def create_img(comment):
    """
    Function:   create_img
    Definition:
    Parameter:  RedditItem
    Return:     NONE
    """
    index = str_comment_list.index(comment)
    num = 0
    if mode == 0:
        alt_font_size = 17
        redesign_footer_font = alt_font_size + 3
    else:
        alt_font_size = 15
        redesign_footer_font = alt_font_size

    # Useful Variables
    line_height = 5
    # Line height and indent are shifted dynamically in the program for simplicity
    line_spacing = 25
    medium_space = 30  # Primarily used to separate footer
    large_space = 40  # Primarily used to separate comments

    image_width = 1920
    indent = 0

    # Fonts used in this function
    body_font = ImageFont.truetype(ui.BODY_FONT_DIR, 20)
    author_font = ImageFont.truetype(ui.AUTHOR_FONT_DIR, alt_font_size)
    time_font = ImageFont.truetype(ui.TIME_FONT_DIR, alt_font_size)
    footer_font = ImageFont.truetype(ui.FOOTER_FONT_DIR, redesign_footer_font)

    if use_reply(comment):
        formatted_reply = reply_list[index].split_self(rWidth)
        rep_len = len(formatted_reply)
        rep_height = large_space + line_spacing * rep_len + medium_space
        rep_score = reply_list[index].score
        rep_author = reply_list[index].author
        rep_time = reply_list[index].time_ago
        rep_gld_icon = reply_list[index].icon

    else:
        rep_height = 0

    if use_rtr(comment):
        formatted_rtr = rtr_list[index].split_self(rtrWidth)
        rtr_len = len(formatted_rtr)
        rtr_height = large_space + line_spacing * rtr_len + medium_space
        rtr_score = rtr_list[index].score
        rtr_author = rtr_list[index].author
        rtr_time = rtr_list[index].time_ago
        rtr_gld_icon = rtr_list[index].icon

    else:
        rtr_height = 0

    formatted_comment = comment_list[index].split_self(cWidth)  # text values are separated into lines,
    com_len = len(formatted_comment)  # this gets the total number of lines

    # Potential comment height; this makes and educated guess at the comments size
    ptnl_com_height = line_height + line_spacing * com_len + medium_space
    img_height = ptnl_com_height + rep_height + rtr_height + medium_space

    img = Image.new('RGBA', (image_width, img_height), ui.IMG_COLOR)
    draw = ImageDraw.Draw(img)

    author = comment_list[index].author
    score = comment_list[index].score
    com_time = comment_list[index].time_ago
    gld_icon = comment_list[index].icon

    # Gets size of several objects for later use
    img_w, img_h = img.size

    # Draws the header for the comment
    def comment_img(fmt_com, auth, scr, tim, gld_icon):
        """
        Function:
        Definition:
        Parameter:
        Return:
        """
        nonlocal line_spacing
        nonlocal line_height
        nonlocal indent
        nonlocal num

        if mode == 1:
            auth = '[–] ' + auth

        formatted_time = f'{tim}'
        formatted_points = f'  {str(text_format.abbreviate_number(scr, 10000))} points  '
        prev_indent = indent
        indent += 40

        if num > 0:
            line_height += large_space

            fttr = ui.CHILD_FOOTER
        else:
            fttr = ui.PARENT_FOOTER

        if num == 1:
            box_hex = '#121212'
        else:
            box_hex = '#161616'
        box_outline_hex = '#333333'

        arrow_indent = indent - 30  # Arrow indent refers to the vote arrow's indentation

        auth_w, auth_h = author_font.getsize(auth)
        scr_w, scr_h = author_font.getsize(formatted_points)
        tm_w, tm_h = author_font.getsize(formatted_time)

        auth_x, auth_y = (indent, line_height)
        scr_x, scr_y = (auth_x + auth_w, line_height)
        tm_x, tm_y = (scr_x + scr_w, line_height)
        gld_x, gld_y = (tm_x + tm_w, line_height)

        if mode == 1:
            draw.rectangle([(prev_indent, line_height - .5*line_spacing), (1920 - 10*num, 15 + line_height + img_height - num*2)],
                           fill=box_hex, outline=box_outline_hex)
        else:
            if num > 0:
                draw.line((indent - 40, img_height - 5, indent - 40, auth_y), fill='#343536', width=5)

        draw.text((auth_x, auth_y), auth, font=author_font, fill=ui.AUTHOR_HEX)
        draw.text((scr_x, scr_y), formatted_points, font=author_font, fill=ui.SCORE_HEX)
        draw.text((tm_x, tm_y), formatted_time, font=time_font, fill=ui.FOOTER_HEX)

        img.paste(ui.COMMENT_VOTE_ICON, (arrow_indent, line_height), ui.COMMENT_VOTE_ICON)
        img.paste(gld_icon, (gld_x, gld_y), gld_icon)

        for line in fmt_com:
            line_height += line_spacing
            line_num = fmt_com.index(line)
            draw.text((indent, line_height), line, font=body_font, fill=ui.BODY_HEX)
            img_path = directories.IMG_DIR + str(index) + '.' + str(num) + '.' + str(line_num) + '.png'

            if line == fmt_com[-1]:
                line_height += medium_space
                draw.text((indent, line_height), fttr, font=footer_font, fill=ui.FOOTER_HEX)

            temp = ui.BACKGROUND.copy()
            temp.paste(img, (0, 540 - int(.5 * img_h)), img)
            temp.save(img_path)

        num += 1

    comment_img(formatted_comment, author, score, com_time, gld_icon)
    if use_reply(comment):
        comment_img(formatted_reply, rep_author, rep_score, rep_time, rep_gld_icon)
    if use_rtr(comment):
        comment_img(formatted_rtr, rtr_author, rtr_score, rtr_time, rtr_gld_icon)

    photofilepath = directories.IMG_DIR + str(index) + '.png'
    # img.show()


def create_txt(comment):
    """
    Function:   create_txt
    Definition: This function takes our gathered text and saves them to a file so that the text can be read by balcon
    Parameter:  Reddit Item
    Return:     NONE
    """
    index = str_comment_list.index(comment)

    filename = directories.TXT_DIR + str(index) + '.0.txt'
    txt_to_save = open(filename, 'w', encoding='utf-8')
    txt_to_save.write(utils.replace_me(comment, aud_rep, aud_rep_with, use_for_audio=True))
    txt_to_save.close()
    if use_reply(comment):
        filename = directories.TXT_DIR + str(index) + '.1.txt'
        txt_to_save = open(filename, 'w', encoding='utf-8')  # for some reason as of 6/17/19 1:10 AM IT NEEDS ENCODING
        txt_to_save.write(utils.replace_me(reply_list[index].body, aud_rep, aud_rep_with, use_for_audio=True))
        txt_to_save.close()
    else:
        pass

    if use_rtr(comment):
        filename = directories.TXT_DIR + str(index) + '.2.txt'
        txt_to_save = open(filename, 'w', encoding='utf-8')  # for some reason as of 6/17/19 1:10 AM IT NEEDS ENCODING
        txt_to_save.write(utils.replace_me(rtr_list[index].body, aud_rep, aud_rep_with, use_for_audio=True))
        txt_to_save.close()
    else:
        pass


def create_wav(comment):
    """
    Function:   create_wav
    Definition: This function creates a command for our text to speech ulility then executes the command,
                this creates a wav file
    Parameter:  RedditItem
    Return:     NONE
    """
    index = str_comment_list.index(comment)

    def balcon(num):
        """
        Function:   balcon
        Definition: This function given a number, creates a command for our command line utiltily
        Parameter:  Integer
        Return:     NONE
        """
        os.chdir(BALCON_DIR)  # changes command line directory for the balcon utility
        txt_file = str(index) + '.%s.txt' % num
        wav_file = str(index) + '.%s.wav' % num
        command = f'balcon -f "Subs\\Sub1\\Txt\\{txt_file}" -w "Subs\\Sub1\\Wav\\{wav_file}" -n "Microsoft Hazel Desktop"'
        os.system(command)
        # logging.info(command)

    balcon(0)
    if use_reply(comment):
        balcon(1)
    else:
        pass
    if use_rtr(comment):
        balcon(2)
    else:
        pass


def create_clip(comment):
    """
    Function:   create_clip
    Definition: The function, given a comment, will create a clip for a given
                The function gathers together the various files needed for video creation such as the image and
                the audio file
    Parameter:  RedditItem
    Return:     VideoClip (moviepy defined class)
    """
    index = str_comment_list.index(comment)

    split_com = comment_list[index].split_self(cWidth)
    split_rep = reply_list[index].split_self(rWidth)
    split_rtr = rtr_list[index].split_self(rtrWidth)

    # Arrays for various clips in sequence
    c_clip = []  # Refers to comment clip ie. the whole this including replies/rtr
    i_clip0 = []
    i_clip1 = []
    i_clip2 = []

    a0_path = directories.WAV_DIR + str(index) + '.0.wav'
    a1_path = directories.WAV_DIR + str(index) + '.1.wav'
    a2_path = directories.WAV_DIR + str(index) + '.2.wav'

    sum_comment_lines = sum(len(line) for line in split_com)
    sum_reply_lines = sum(len(line) for line in split_rep)
    sum_rtr_lines = sum(len(line) for line in split_rtr)

    a_clip0 = AudioFileClip(a0_path)
    a_clip0 = concatenate_audioclips([a_clip0, SILENCE])

    for string in split_com:
        factor = len(string) / sum_comment_lines
        path = directories.IMG_DIR + str(index) + '.0' + '.%s.png' % split_com.index(string)
        clip = ImageClip(path).set_duration(factor * a_clip0.duration)
        i_clip0.append(clip)
        # logging.info(path)

    s0 = '\ndone comment: ' + str(index)
    i_clip0 = concatenate_videoclips(i_clip0)
    i_clip0 = i_clip0.set_audio(a_clip0)
    c_clip.append(i_clip0)

    if use_reply(comment):
        a_clip1 = AudioFileClip(a1_path)
        a_clip1 = concatenate_audioclips([a_clip1, SILENCE])
        for rString in split_rep:
            factor = len(rString) / sum_reply_lines
            path = directories.IMG_DIR + str(index) + '.1' + '.%s.png' % split_rep.index(rString)
            clip = ImageClip(path).set_duration(factor * a_clip1.duration)
            i_clip1.append(clip)
            # logging.info(path)

        s1 = '\n\tdone reply: ' + str(index)
        i_clip1 = concatenate_videoclips(i_clip1)
        i_clip1 = i_clip1.set_audio(a_clip1)
        c_clip.append(i_clip1)
    else:
        s1 = ''
        pass

    if use_rtr(comment):
        a_clip2 = AudioFileClip(a2_path)
        a_clip2 = concatenate_audioclips([a_clip2, SILENCE])
        for rtrString in split_rtr:
            factor = len(rtrString) / sum_rtr_lines
            path = directories.IMG_DIR + str(index) + '.2' + '.%s.png' % split_rtr.index(rtrString)
            clip = ImageClip(path).set_duration(factor * a_clip2.duration)
            i_clip2.append(clip)
            # logging.info(path)
        s2 = '\n\t\tdone rtr: ' + str(index)
        i_clip2 = concatenate_videoclips(i_clip2)
        i_clip2 = i_clip2.set_audio(a_clip2)
        c_clip.append(i_clip2)
    else:
        s2 = ''
        pass
    c_clip.append(TRANSITION)
    c_clip = concatenate_videoclips(c_clip)
    print(s0, end='')
    print(s1, end='')
    print(s2, end='')
    return c_clip


def create_sub():
    """
    Function:   create_sub
    Definition: This function combines all steps previously done
                The function creates an image for the submission, converts the body text of the post to audio,
                then, the program creates a clip from the photo and audio
    Parameter:  NONE
    Return:     NONE
    """
    size = 20
    width = 180
    subreddit = str(reddit_post.subreddit)
    body_nolinks = re.sub(r"\[(.+)\]\(.+\)", r"\1", reddit_post.body)
    body_nolinks = re.sub(r'https?:\/\/.*[\r\n]*', '', body_nolinks)
    body_nolinks = utils.replace_me(body_nolinks, all_rep, all_rep_with)

    author_font = ImageFont.truetype(ui.AUTHOR_FONT_DIR, 15)
    score_font = ImageFont.truetype(ui.SCORE_FONT_DIR, size - 3)
    title_font = ImageFont.truetype(ui.TITLE_FONT_DIR, size)
    body_font = ImageFont.truetype(ui.BODY_FONT_DIR, size - 2)
    sub_font = ImageFont.truetype(ui.SUB_FONT_DIR, size - 6)
    footer_font = ImageFont.truetype(ui.FOOTER_FONT_DIR, size - 6)

    formatted_title = textwrap.wrap(reddit_post.title, width=width)
    formatted_body = textwrap.wrap(body_nolinks, width=width + 8)
    post_date_by = 'submitted ' + text_format.human_time(reddit_post.created) + ' by '

    formatted_points = str(text_format.abbreviate_number(reddit_post.score)).replace('.0', '')

    # Specify all variables
    line_spacing = 28
    more_spacing = line_spacing
    small_space = 5
    medium_space = 12
    large_space = 35
    indent_spacing = 65
    line_height = 0
    sub_height = (15 + line_height + len(formatted_title) * line_spacing + 2 * small_space + large_space +
                  len(formatted_body) * line_spacing + 2 * medium_space)

    sub_img = Image.new('RGBA', (1920, sub_height), ui.IMG_COLOR)  # from #222222
    sub_draw = ImageDraw.Draw(sub_img)

    # Draws rectangle at current height
    sub_draw.rectangle(
        [(indent_spacing, line_height), (1920 - 10,
                                         15 + line_height + len(
                                             formatted_title) * line_spacing + 2 * small_space + large_space
                                         + len(formatted_body) * line_spacing + 2 * medium_space)], fill='#373737')

    # Draws the score and icon
    point_len = len(formatted_points.replace('.', ''))
    indent = 5 * (5 - point_len)
    sub_img.paste(ui.SUB_SCORE_ICON, (15, line_height + 2), ui.SUB_SCORE_ICON)
    sub_draw.text((indent, line_height + 26), formatted_points, font=score_font, fill=ui.BIG_SCORE_HEX)

    # Writes each line in the title @
    for line in formatted_title:
        sub_draw.text((indent_spacing, line_height), line, font=title_font, fill=ui.TITLE_HEX)
        if line == formatted_title[-1]:
            the_sizex, the_sizey = title_font.getsize(formatted_title[-1])
            sub_draw.text((indent_spacing + the_sizex + 5, line_height + 5), f'(self.{str(reddit_post.subreddit)})',
                          font=sub_font, fill='#888888')
        line_height = line_height + line_spacing
    del line

    # Adds spacing then writes the post date and author
    line_height += small_space
    sub_draw.text((indent_spacing, line_height), post_date_by, font=author_font, fill=ui.TIME_HEX)
    rrx, rry = author_font.getsize(post_date_by)
    sub_draw.text((indent_spacing + rrx, line_height), ' ' + str(reddit_post.author), font=author_font, fill=ui.AUTHOR_HEX)
    line_height += small_space

    temp = ui.BACKGROUND.copy()

    filename = directories.TXT_DIR + 'title.txt'
    with open(filename, 'w', encoding='utf-8') as title_txt:  # for some reason as of 6/17/19 1:10 AM IT NEEDS ENCODING
        title_txt.write(utils.replace_me(reddit_post.title, aud_rep, aud_rep_with, use_for_audio=True))

    formatted_sub = subreddit.replace('_', ' ').replace('AmItheAsshole', 'Am I The Asshole')
    formatted_sub = re.sub(r"(\w)([A-Z])", r"\1 \2", formatted_sub)
    formatted_sub = f'r/ {formatted_sub}'

    with open(directories.TXT_DIR + 'sub_text.txt', 'w', encoding='utf-8') as sub_txt:
        sub_txt.write(formatted_sub)

    os.chdir(BALCON_DIR)  # changes command line directory for the balcon utility
    txt_file = 'title.txt'
    wav_file = 'title.wav'
    balcom = f'balcon -f "Subs\\Sub1\\Txt\\{txt_file}" -w "Subs\\Sub1\\Wav\\{wav_file}" -n "Microsoft Hazel Desktop"'
    os.system(balcom)
    while not os.path.isfile(directories.WAV_DIR + 'title.wav'):
        time.sleep(.12)

    os.chdir(BALCON_DIR)  # changes command line directory for the balcon utility
    txt_file = 'sub_text.txt'
    wav_file = 'sub_text.wav'
    balcom = f'balcon -f "Subs\\Sub1\\Txt\\{txt_file}" -w "Subs\\Sub1\\Wav\\{wav_file}" -n "Microsoft Hazel Desktop"'
    os.system(balcom)
    while not os.path.isfile(directories.WAV_DIR + 'sub_text.wav'):
        time.sleep(.12)

    sub_aclip = AudioFileClip(directories.WAV_DIR + 'sub_text.wav')
    title_aclip = AudioFileClip(directories.WAV_DIR + 'title.wav')
    title_aclip = concatenate_audioclips([sub_aclip, SILENCE, title_aclip, SILENCE])

    if reddit_post.body != '':
        # Draws a rectangle at line spacing + large space
        # large_space - small_space is used to negate the previous addition to line height
        len_body = len(formatted_body)
        line_height += large_space
        sub_draw.rectangle([indent_spacing, line_height - medium_space, 1920 - 100, small_space + line_height +
                            len_body * line_spacing], fill=None, outline='#cccccc', width=1)

        body_iclips = []

        filename = directories.TXT_DIR + 'body.txt'
        body_txt_file = open(filename, 'w',
                              encoding='utf-8')  # for some reason as of 6/17/19 1:10 AM IT NEEDS ENCODING
        body_txt_file.write(utils.replace_me(body_nolinks, aud_rep, aud_rep_with, use_for_audio=True))
        body_txt_file.close()

        os.chdir(BALCON_DIR)  # changes command line directory for the balcon utility
        txt_file = 'body.txt'
        wav_file = 'body.wav'
        balcom = f'balcon -f "Subs\\Sub1\\Txt\\{txt_file}" -w "Subs\\Sub1\\Wav\\{wav_file}" -n "Microsoft Hazel Desktop"'
        os.system(balcom)
        while not os.path.isfile(directories.WAV_DIR + 'body.wav'):
            time.sleep(.12)
        body_aclip = AudioFileClip(directories.WAV_DIR + 'body.wav')

        sum_body = sum(len(fff) for fff in formatted_body)

        temp.paste(sub_img, (0, 540 - int(.5 * sub_height)), sub_img)
        temp.save(directories.IMG_DIR + 'title.png')
        title_vclip = ImageClip(directories.IMG_DIR + 'title.png').set_audio(title_aclip).set_duration(title_aclip.duration)

        # Creates Text Body
        for line in formatted_body:
            index = formatted_body.index(line)
            sub_draw.text((indent_spacing + 10, line_height), line, font=body_font, fill='#dddddd')
            line_height = line_height + line_spacing

            if line == formatted_body[-1]:
                line_height += medium_space
                sub_draw.text((indent_spacing, line_height), ui.TITLE_FOOTER, font=footer_font, fill=ui.FOOTER_HEX)
            temp.paste(sub_img, (0, 540 - int(.5 * sub_height)), sub_img)

            temp.save(directories.IMG_DIR + f'body.{index}.png')

            factor = len(line)/sum_body
            # logging.info(str(factor))
            body_iclips.append(ImageClip(directories.IMG_DIR + f'body.{index}.png').set_duration(factor * body_aclip.duration))
        del line

        body_iclip = concatenate_videoclips(body_iclips)
        body_vclip = body_iclip.set_audio(body_aclip)
        body_vclip = concatenate_videoclips([title_vclip, body_vclip, TRANSITION])

        return body_vclip
    else:
        # Places Space Then Draws Footer
        line_height += medium_space + more_spacing
        sub_draw.text((indent_spacing, line_height), ui.TITLE_FOOTER, font=footer_font, fill=ui.FOOTER_HEX)

        temp.paste(sub_img, (0, 540 - int(.5 * sub_height)), sub_img)
        temp.save(directories.IMG_DIR + 'title.png')

        title_iclip = ImageClip(directories.IMG_DIR + 'title.png').set_duration(title_aclip.duration)
        title_vclip = title_iclip.set_audio(title_aclip)
        title_vclip = concatenate_videoclips([title_vclip, TRANSITION])
        return title_vclip


def cleanup():
    """
    Function:   cleanup()
    Definition: This function deletes all directions involved in the creation of the video
                (excluding supplementary directories that house the fonts and icons)
                The function also recreates the directories, however, they will be empty
                the function also contains a global variable del_vid which determines whether we delete the video
    Parameter:  NONE
    Return:     NONE
    """
    global del_vid
    shutil.rmtree(directories.IMG_DIR)
    logging.info('Removed IMG')
    time.sleep(.05)
    os.mkdir(directories.IMG_DIR)
    logging.info("Created IMG")

    shutil.rmtree(directories.TXT_DIR)
    logging.info('Removed TXT')
    time.sleep(.05)
    os.mkdir(directories.TXT_DIR)
    logging.info('Created TXT')

    shutil.rmtree(directories.WAV_DIR)
    logging.info('Removed WAV')
    time.sleep(.05)
    os.mkdir(directories.WAV_DIR)
    logging.info('Created WAV')

    if os.path.isfile('Upload/Final.mp4'):
        os.remove('Upload/Final.mp4')
        logging.info('Removed Vid Copy')
    if os.path.isfile('Upload/thumb.png'):
        os.remove('Upload/thumb.png')
        logging.info('Removed Thumb Copy')
    if not os.path.isdir(directories.VID_DIR):
        os.mkdir(directories.VID_DIR)
        logging.info("VID DNE ... Making VID")
    if del_vid and os.path.isdir(directories.VID_DIR):
        shutil.rmtree(directories.VID_DIR)
        logging.info('Removed VID')
        time.sleep(.05)
        os.mkdir(directories.VID_DIR)
        logging.info("Created VID")

    del_vid = False


def create_thumbnail():
    """
    Function:   create_thumbnail
    Definition: This function uses the PIL Library to draw a easily readable thumbnail
    Parameter:  NONE
    Return:     NONE
    """
    def color_options():
        """
        Function:   color_options
        Definition: Accepts user input for preferred ui.BACKGROUND color
        Parameter:  NONE
        Return:     NONE
        """
        global bgrd_choice

        if bgrd_choice == 0:
            color = 0
        elif bgrd_choice == 1:
            color = '#222222'
        elif bgrd_choice == 2:
            color = 'black'
        else:
            logging.info('Choice is not recognized reverting to defaults')
            color = '#222222'
        return color

    # date = datetime.datetime.fromtimestamp(submission.created_utc)
    # dif = datetime.datetime.utcnow() - date
    # logging.info(dif)

    sub_time = reddit_post.created
    subreddit = 'r/' + str(reddit_post.subreddit)
    author = 'u/' + str(reddit_post.author)
    score = int(reddit_post.score)
    num_com = int(reddit_post.num_com)
    title = reddit_post.title.replace('/', ' ').replace('[', '').replace(']', '')
    if cust_title != '0':
        title = cust_title
    thumbnail = Image.new('RGBA', (1920, 1080), color_options())  # from #222222
    thumb_draw = ImageDraw.Draw(thumbnail)
    width = 31
    formatted_title = textwrap.wrap(title, width=width)

    icon_w, icon_h = ui.ASKREDDIT_ICON.size

    size = 90
    sub_font = ImageFont.truetype('CustFont/NimbusSanL-Reg.ttf', 75)
    author_font = ImageFont.truetype('CustFont/NimbusSanL-Bol.ttf', 45)
    score_font = ImageFont.truetype('CustFont/NimbusSanL-Bol.ttf', 60)

    base_height = 210
    line_spacing = 90
    indent_spacing = 40
    point_x, point_y = -40, 720

    # thumbnail.paste(ui.COMMENT_ICON, (300, 850), ui.COMMENT_ICON)
    # thumbnail.paste(ui.UPDOWNVOTE, (point_x, point_y), ui.UPDOWNVOTE)
    thumbnail.paste(ui.ASKREDDIT_ICON, (40, 40), ui.ASKREDDIT_ICON)

    thumb_draw.text((icon_w + indent_spacing + 30, 120), f'submitted {text_format.human_time(sub_time)} by {author}',
                    font=author_font, fill='#818384')

    thumb_draw.text((icon_w + indent_spacing + 30, 40), subreddit, font=sub_font)
    # thumb_draw.text((90, 910), str(text_format.abbreviate_number(score)), font=score_font, fill='#FF8C60')
    # thumb_draw.text((500, 900), str(text_format.abbreviate_number(num_com)) + '  Comments', font=score_font, fill='#818384')

    line_height_thumb = base_height
    # logging.info(str(len(formatted_title) * (size + line_spacing)))
    count_1 = 0
    count_2 = 0
    min_b, max_b = 1180, 1400  # From 1020, 1200
    while not min_b <= len(formatted_title) * (size + line_spacing) <= max_b:
        while len(formatted_title) * (size + line_spacing) >= max_b:
            count_1 = count_1 + 1
            size = size - 2
            line_spacing = line_spacing - 2
            width = width + .8
            formatted_title = textwrap.wrap(title, width=width)
            if count_1 >= 35:
                break
        while len(formatted_title) * (size + line_spacing) <= min_b:
            count_2 = count_2 + 1
            size = size + 2
            line_spacing = line_spacing + 2
            width = width - .8
            formatted_title = textwrap.wrap(title, width=width)
            if count_2 >= 35:
                break
        if count_1 >= 35:
            break
        if count_2 >= 35:
            break
    # logging.info(str(len(formatted_title) * (size + line_spacing)))
    # logging.info(count_1, count_2)
    for line in formatted_title:
        body_font = ImageFont.truetype('CustFont/American_Captain.ttf', size)

        draw_outlined_text(indent_spacing, line_height_thumb, thumb_draw, body_font, line, width=3)

        line_height_thumb = line_height_thumb + line_spacing

    # thumbnail.show()
    thumbnail.save(directories.VID_DIR + 'thumb.png')

    # draw.text((indent, com_img_height - 25), footer_parent, font=author_font, fill="#828282")
    # img.paste(commentUpDownIcon, (arrow_indent, 13), commentUpDownIcon)


def data_collection():
    """
    Function:   data_collection
    Definition: Appends all function data to a csv file
    Parameter:  NONE
    Return:     NONE
    """
    csv_row = [str(get_sum_chars()), str(final.duration), str(number_comments), str(threshold), str(datetime.datetime.now()),
               str(reddit_link)]
    with open('program_data.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_row)


def dynamic_music():
    """
    Function:   dynamic_music
    Definition: This function reads all mp3 files in the dynamic music directory and shuffles them.
                The info on the shuffled list is also saved for the description.
                The lower bound for the lengths of the concatenated songs will be the estimated time * 1.1.
    Parameter:  NONE
    Return:     NONE
    """
    global song_sound
    global sound_desc
    song_sound = []
    song_info = []
    temp = os.path.dirname(os.path.abspath('Static/DynamicMusic/DynamicMusic.txt')) + '\\*.mp3'
    dynam_dir = glob.glob(temp)
    shuffle(dynam_dir)
    dur_counter = 0
    for song in dynam_dir:
        mp3 = MP3File(song)
        mp3.set_version(VERSION_2)
        artist = mp3.__getattribute__('artist')
        title = mp3.__getattribute__('song')

        index = dynam_dir.index(song)
        song_sound.append(AudioFileClip(song))
        dur_counter = dur_counter + song_sound[index].duration

        info = '\nSong: ' + title + \
               '\nArtist:  ' + artist + \
               '\nTimestamp: ' + text_format.minute_format(dur_counter - song_sound[index].duration, 0) + \
               '\n'
        song_info.append(info)

        if dur_counter > estimated_time * 1.1:
            break
    song_sound = concatenate_audioclips(song_sound)
    song_sound = song_sound.volumex(.0875)
    sound_desc = ''.join(song_info)


df = pd.read_csv('MLData.csv')
reg = linear_model.LinearRegression()
reg.fit(df[['char_len', 'num_com', 'threshold']], df.duration)


def estimate_time(char_sum):
    """
    Function:   estimate_time
    Definition: Adds up the total number of characters in the entirity of the video and comes up with a time
                estimate in seconds.
    Parameter:  Integer
    Return:     Double
    """
    x = round(reg.predict([[char_sum, number_comments, threshold]])[0], 5)
    return x


def video_creation(comment):
    """
    Function:   video_creation
    Definition: Thus appends clips to the clip array, the function also makes sure the files neccesary have
                already been created
    Parameter:  RedditItem
    Return:     NONE
    """
    index = str_comment_list.index(comment)
    create_txt(comment)
    create_wav(comment)
    create_img(comment)
    # createAudioClip(comment)
    sp0 = directories.WAV_DIR + str(index) + '.0.wav'
    sp1 = directories.WAV_DIR + str(index) + '.1.wav'
    sp2 = directories.WAV_DIR + str(index) + '.2.wav'
    # logging.info(sp0)
    # logging.info(sp1)
    # logging.info(sp2)
    while not os.path.isfile(sp0):
        logging.info(sp0)
        time.sleep(.3)
        logging.info("waiting for comment:" + str(index))
    if use_reply(comment):
        while not os.path.isfile(sp1):
            time.sleep(.3)
            logging.info("waiting for reply:" + str(index))
    else:
        pass
    if use_rtr(comment):
        while not os.path.isfile(sp2):
            time.sleep(.3)
            logging.info("waiting for comment:" + str(index))
    else:
        pass
    # time.sleep(3)
    main_clips.append(create_clip(comment))


def metadata():
    """
    Function:   metadata
    Definition: generates video metadata and writes it to a file
    Parameter:  NONE
    Return:     NONE
    """
    str_tag = (
        'reddit, best of ask reddit, reddit, ask reddit top posts, r/story, r/ askreddit, r/askreddit, story time, '
        'reddify, bamboozled, brainydude, '
        'reddit watchers, best posts & comments, reddit, askreddit, USER'
    )
    data = {
        'title': reddit_post.title + ' (r/AskReddit)',
        'description': f'r/{str(reddit_post.subreddit)} Videos! Welcome back to a brand new USER video!'
                       '\n\n Dont forget to like and subscribe'
                       '\n'
                       '\n I love to upload New daily videos to keep yall entertained'
                       '\n'
                       '\n🎧♪♫ [Track List] ♫♪🎧 '
                       f'\n{sound_desc}\n'
                       '\nOutro Template made by Grabster - Youtube.com/GrabsterTV'
                       '\n'
                       f'\nSubreddits used: r/{str(reddit_post.subreddit)}'
                       '\n'
                       '\n#reddit #askreddit #askredditscary'
                       '\n'
                       '\n--- Tags ---'
                       '\n' + str_tag,
        'tags': [x.strip() for x in str_tag.split(',')],
        'privacyStatus': 'private',
        # 'embeddable': 'true',
        # 'license': "creativeCommon",
        # 'publicStatsViewable': 'true',
        # 'publishAt': '2017-06-01T12:05:00+02:00',
        # 'categoryId': '10',
        # 'recordingdate': str(datetime.date),
        # 'location': {
        #     'latitude': 48.8584,
        #     'longitude': 2.2945
    }
    # logging.info(data['description'])
    with open(UPLOAD_DIR + 'data.json', 'w') as f:
        json.dump(data, f)
    with open(directories.VID_DIR + 'description.txt', 'w', encoding='utf-8') as desc:
        desc.write(data['description'])


def upload_video():
    """
    ** WORK IN PROGRESS **
    Function:   upload video
    Definition: The program create a command to run the upload to youtube command line utility
    Parameter:  NONE
    Return:     NONE
    """
    shutil.copy2(video_path, UPLOAD_DIR)
    shutil.copy2(directories.VID_DIR + 'thumb.png', UPLOAD_DIR)
    command = []
    os.chdir(UPLOAD_DIR)
    command.append('youtubeuploader_windows_amd64 ')
    command.append('-filename ' + vid_name + vid_extension + ' ')
    command.append('-thumbnail ' + 'thumb.png ')
    command.append('-metaJSON string ' + 'data.json')
    command = ''.join(command)
    os.system(command)
    logging.info(command)


def get_sum_chars():
    """
    Function:   get_sum_chars
    Definition: This function uses the currently set number of comments and threshold (indirectly) to determine the
                sum of the charaters that we plan to use.
    Parameter:  NONE
    Return:     Integer
    """
    char_sum = len(str(reddit_post.title)) + len(reddit_post.body)
    for x in str_comment_list[:number_comments]:
        gh = str_comment_list.index(x)
        char_sum = char_sum + len(x)
        if use_reply(x):
            char_sum = char_sum + len(reply_list[gh].body)
        else:
            pass
        if use_rtr(x):
            char_sum = char_sum + len(rtr_list[gh].body)
        else:
            pass
    return char_sum

if __name__ == '__main__':
    # Initialize useful lists
    main_clips = []
    comment_list = []
    str_comment_list = []
    reply_list = []
    rtr_list = []
    # Replacement lists
    aud_rep, aud_rep_with = ['’', '‘', '”', '“', '*', ';', '^', '\\', '/', '_'], \
                            ["'", "'", '"', '"', '', '', '', '', '', ' ']
    viz_rep, viz_rep_with = [], []
    all_rep, all_rep_with = ['&#x200B'], ['']

    # if these values are not changed the tts engine will read the arcronyms, leading to mispronunciations
    aita_1, aita_2 = utils.insensitive_replace_list(
        ['aita', 'yta', 'nta', 'esh'],
        ['am i the asshole', 'you\'re the asshole', 'not the asshole', 'everyone sucks here']
    )

    # if these values are not changed the tts engine will read the arcronyms, leading to mispronunciations
    sms_1, sms_2 = utils.insensitive_replace_list(
        ['lol ', 'lol.', 'jk', 'smh', 'stfu', 'nvm', 'tbh', 'tifu'],
        ['el oh el', 'el oh el.', 'just kidding', 'shake my head', 'shut the fuck up', 'nevermind', 'to be honest', 'today i fucked up']
    )

    # These are words that the TTS engine often mispronounces
    common_mispronunciations_1, common_mispronunciations_2 = utils.insensitive_replace_list(
        ['coworker', 'facebook'],
        ['co-worker', 'face book']
    )
    # Censors swear words
    swear_1, swear_2 = utils.insensitive_replace_list(
        ['fuck', 'shit', 'bitch'],
        ['uck', 'sit', 'itch']
    )

    # Appends replacement lists in a way that saves space
    aud_rep.extend(aita_1)
    aud_rep_with.extend(aita_2)
    aud_rep.extend(sms_1)
    aud_rep_with.extend(sms_2)
    all_rep.extend(swear_1)
    all_rep_with.extend(swear_2)

    del_vid = True
    cleanup()


    create_thumbnail()
    # Pulls data for the program from Reddit at once
    populate_lists()

    # This block is used for getting the video length within a certain range
    estimated_time = estimate_time(get_sum_chars())
    logging.info(f'\nMaximum Video Length is: {text_format.minute_format(estimated_time)} or {str(estimated_time)}s')

    if desired_vid_len > estimated_time:
        desired_vid_len = estimated_time
        logging.info(f'\nInput exceeds maximum time of {estimated_time}s for this reddit post, setting time to {estimated_time}')

    while estimate_time(get_sum_chars()) > desired_vid_len:
        number_comments -= 1
        if estimate_time(get_sum_chars()) <= desired_vid_len:
            break

        threshold += .04
        if estimate_time(get_sum_chars()) <= desired_vid_len:
            break

        if threshold > .8:
            threshold = .3      # reset threshold if it gets too high


    estimated_time = estimate_time(get_sum_chars())

    logging.info(f'Estimated Video Length is: {text_format.minute_format(estimated_time)} or {str(estimated_time)}s')
    logging.info(f'Number of Comments: {number_comments}')
    logging.info(f'Threshold: {threshold}')
    logging.info(f'Subreddit: {reddit_post.subreddit}')

    dynamic_music()

    final = [create_sub()]

    # Used for multithreading purposes if the option is selected
    thread = []  # 'thread' is used to keep track of all running threads so that they can be joined
    if speed == 0:
        for com in str_comment_list[:number_comments]:
            ind = str_comment_list.index(com)
            temp_thread = threading.Thread(target=video_creation, args=(com,))
            thread.append(temp_thread)
            thread[ind].start()

        for com in str_comment_list[:number_comments]:
            ind = str_comment_list.index(com)
            thread[ind].join()

    else:
        for com in str_comment_list[:number_comments]:
            video_creation(com)

    # This combines all the clips created in the multithreaded workload to one video and sets the audio to the dynamic audio
    shuffle(main_clips)
    final.extend(main_clips)
    final.append(OUTRO)
    final = concatenate_videoclips(final)
    ui.BACKGROUND_music = song_sound.set_duration(final.duration)
    final_audio = CompositeAudioClip([final.audio, ui.BACKGROUND_music])
    final = final.set_audio(final_audio)

    # Used to compare the estimated video length the the actual length
    pct_diff = round(100 - (abs(estimated_time / final.duration) * 100), 2)
    if pct_diff > 0:
        pct_diff = '+' + str(pct_diff)
    else:
        pct_diff = str(pct_diff)
    abs_diff = final.duration - estimated_time
    formatted_diff = text_format.minute_format(abs_diff)
    if float(abs_diff) > 0:
        formatted_diff = '+' + formatted_diff
    else:
        pass

    logging.info(f'\n \nActual Video Length is: {text_format.minute_format(final.duration)} / {str(final.duration)}s. '
        f'Shifted {formatted_diff} / {str(pct_diff)}% from {text_format.minute_format(estimated_time)} / {str(estimated_time)}s\n')

    vid_name = str(submission.id)
    vid_extension = '.mp4'
    video_path = directories.VID_DIR + vid_name + vid_extension
    final.write_videofile(video_path, fps=VID_FPS, threads=16, preset='ultrafast')

    metadata()
    # upload_video()

    # Collects data to help improve the program's predictions
    data_collection()
    logging.info('\n')
    cleanup()

    logging.info('\nClosing in 10 seconds')
    time.sleep(10)
