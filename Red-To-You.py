import praw
from moviepy.editor import *
from PIL import Image, ImageFont, ImageDraw
import textwrap
import time
import datetime
import shutil
import re
import glob
from random import shuffle
import threading
import timeit
import json
import csv
import pandas as pd  # need pip
from sklearn import linear_model  # need pip
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
import itertools

# User Input
mode = int(input('Mode; 0 = Redesign, 1 = Classic '))
speed = int(input('\nSpeed; 0 = Multithreaded, 1 = Normal '))
reddit_link = input('\nLink; Paste your desired reddit post:\n')
desired_vid_len = int(input('\nTime; Enter your maximum desired video length (seconds): '))
bgrd_choice = int(input('\nColor; Type your background color option [0 = Transparent, 1 = Default, 2 = Black]: '))
cust_title = input('\nTitle; Type a custom title for thumbnails, to  use default type 0\n')

# Reddit Setup
reddit = praw.Reddit(client_id='BHUtkEY0x4vomA', client_secret='MZvTVUs83p8wEN_Z8EU8bIUjGTY',
                     user_agent='pulling posts')
submission = reddit.submission(url=reddit_link)


class RedditTitle:
    title = submission.title
    body = submission.selftext
    author = submission.author
    subreddit = submission.subreddit
    score = submission.score
    created = datetime.datetime.fromtimestamp(submission.created)
    num_com = submission.num_comments
    try:
        author = submission.author.name
    except:
        author = '[deleted]'

    def split_self(self, width):
        """
        Function:   split_self
        Definition: Takes a long string and splits the string into lines of length width
        Parameter:  width
        Return:     List
        """
        split = textwrap.wrap(self.title, width=width)
        return split


class RedditItem(object):
    # Imported with Pillow - Gildings
    gild_w, gild_h = (20, 20)
    PLATINUM = Image.open('Static/platinum.png')
    PLATINUM = PLATINUM.resize((gild_w, gild_h), Image.ANTIALIAS)
    GOLD = Image.open('Static/gold.png')
    GOLD = GOLD.resize((gild_w, gild_h), Image.ANTIALIAS)
    SILVER = Image.open('Static/silver.png')
    SILVER = SILVER.resize((gild_w, gild_h), Image.ANTIALIAS)
    icon_img_font = ImageFont.truetype('CustFont/verdanab.ttf', 17)

    def __init__(self, string, author, score, time_ago, gildings):
        self.string = string
        self.author = author
        self.score = score
        self.time_ago = time_ago
        self.gildings = gildings

        if 'gid_1' in self.gildings:
            num_silver = self.gildings['gid_1']
        else:
            num_silver = 0
        if 'gid_2' in self.gildings:
            num_gold = self.gildings['gid_2']
        else:
            num_gold = 0
        if 'gid_3' in self.gildings:
            num_platinum = self.gildings['gid_3']
        else:
            num_platinum = 0

        icon_img = Image.new('RGBA', (200, self.gild_h), (0, 0, 0, 0))  # self.gild_h
        icon_img_draw = ImageDraw.Draw(icon_img)
        icon_img_height = self.gild_h
        text_height = -3
        small_spacing = 3
        spacing = 9
        current_width = 0

        more_space = 0
        if num_silver >= 1:
            icon_img.paste(self.SILVER, (current_width, 0), self.SILVER)
            current_width += self.gild_w
            more_space = spacing
        if num_silver >= 2:
            current_width += small_spacing
            icon_img_draw.text((current_width, text_height), str(num_silver), font=self.icon_img_font, fill='#6a98af')
            current_width += spacing
        current_width += more_space
        more_space = 0
        if num_gold >= 1:
            icon_img.paste(self.GOLD, (current_width, 0), self.GOLD)
            current_width += self.gild_w
            more_space = spacing
        if num_gold >= 2:
            current_width += small_spacing
            icon_img_draw.text((current_width, text_height), str(num_gold), font=self.icon_img_font, fill='#6a98af')
            current_width += spacing
        current_width += more_space
        if num_platinum >= 1:
            icon_img.paste(self.PLATINUM, (current_width, 0), self.PLATINUM)
            current_width += self.gild_w
        if num_platinum >= 2:
            current_width += small_spacing
            icon_img_draw.text((current_width, text_height), str(num_platinum), font=self.icon_img_font, fill='#6a98af')
            current_width += spacing

        self.icon = icon_img

    def split_self(self, width):
        """
        Function:   split_self
        Definition: Takes a long string and splits the string into lines of length width
        Parameter:  width
        Return:     List
        """
        split = textwrap.wrap(self.string, width=width)
        return split

    def get_split_len(self, width):
        """
        Function:   get_split_len
        Definition: returns the length of a string that was split
        Parameter:  width
        Return:     Integer
        """
        split_len = textwrap.wrap(self.string, width=width)
        return len(split_len)


number_comments = 25  # int(input('Type a Number Between 1 and 25 to represent the Number of Comments\n'))
threshold = .3  # float(input('Type a number between 0 and 1 to represent the reply threshold (.33 recommended) \n'))
MIN_SCORE = 50
DNE = 'Does Not Exist'

# Keep static, folders deleted on exit
IMG_DIR = 'Subs/Sub1/Img/'
WAV_DIR = 'Subs/Sub1/Wav/'
TXT_DIR = 'Subs/Sub1/Txt/'
VID_DIR = 'Subs/Vid/'

# EXE Directories
BALCON_DIR = os.path.dirname(os.path.abspath("balcon.exe"))
UPLOAD_DIR = os.path.dirname(os.path.abspath('Upload/youtubeuploader_windows_amd64.exe')) + '\\'

cWidth = 175    # Width between comments
rWidth = 168    # Width between replies
rtrWidth = 161  # Width between replies to replies
VID_FPS = 15    # Video frames per second

# Imported with Pillow
BACKGROUND = Image.open('Static/backgroundblack.jpg').convert('RGBA')
if mode == 0:
    COMMENT_VOTE_ICON = Image.open('Static/commentupdown_2.png').convert('RGBA')
else:
    COMMENT_VOTE_ICON = Image.open('Static/commentupdown.png').convert('RGBA')
COMMENT_VOTE_ICON = COMMENT_VOTE_ICON.resize((22, 56), Image.ANTIALIAS)
TITLE_VOTE_ICON = Image.open('Static/titleupdown.png').convert('RGBA')
COMMENT_VOTE_ICON = COMMENT_VOTE_ICON  # Revisit Later
SUB_SCORE_ICON = Image.open('Static/sub_up_down.png').convert('RGBA')
SUB_SCORE_ICON = SUB_SCORE_ICON.resize((28, 73), Image.ANTIALIAS)
# Imported with Pillow - Thumbnail Items
ASKREDDIT_ICON = Image.open('Thumbnail/askreddit.png').resize((100, 100), Image.ANTIALIAS)  # move later
UPDOWNVOTE = Image.open('Thumbnail/upvotedownvote.png').convert('RGBA')
UPDOWNVOTE = UPDOWNVOTE.resize((440, 400), Image.ANTIALIAS)
COMMENT_ICON = Image.open('Thumbnail/commenticon.png')
COMMENT_ICON = COMMENT_ICON.resize((180, 160), Image.ANTIALIAS)

if mode == 0:
    TITLE_FONT_DIR = 'CustFont/noto-sans/NotoSans-Medium.ttf'
    BODY_FONT_DIR = 'CustFont/noto-sans/NotoSans-Regular.ttf'
    SUB_FONT_DIR = 'CustFont/IBM_TTF/IBMPlexSans-Bold.ttf'
    AUTHOR_FONT_DIR = 'CustFont/IBM_TTF/IBMPlexSans-Regular.ttf'
    TIME_FONT_DIR = 'CustFont/IBM_TTF/IBMPlexSans-Regular.ttf'
    FOOTER_FONT_DIR = 'CustFont/IBM_TTF/IBMPlexSans-Bold.ttf'
    SCORE_FONT_DIR = 'CustFont/IBM_TTF/IBMPlexSans-Regular.ttf'

    # Lists all the hex code for fill
    AUTHOR_HEX = '#4fbcff'
    SCORE_HEX = '#818384'
    TIME_HEX = '#818384'
    BODY_HEX = '#d7dadc'
    FOOTER_HEX = '#818384'
    TITLE_HEX = '#d7dadc'
    BIG_SCORE_HEX = '#818384'

    TITLE_FOOTER = str(RedditTitle.num_com) + ' Comments   Give Award   Share'
    PARENT_FOOTER = 'Reply   Give Award  Share   Report   Save'
    CHILD_FOOTER = PARENT_FOOTER
    IMG_COLOR = '#1a1a1b'

else:
    # Lists font Directories
    TITLE_FONT_DIR = 'CustFont/Verdana.ttf'
    BODY_FONT_DIR = 'CustFont/Verdana.ttf'
    SUB_FONT_DIR = 'CustFont/Verdana.ttf'
    AUTHOR_FONT_DIR = 'CustFont/verdanab.ttf'
    TIME_FONT_DIR = 'CustFont/verdana.ttf'
    FOOTER_FONT_DIR = 'CustFont/verdanab.ttf'
    SCORE_FONT_DIR = 'CustFont/verdanab.ttf'

    # Lists all the hex code for fill
    AUTHOR_HEX = '#6a98af'
    SCORE_HEX = '#b4b4b4'
    TIME_HEX = '#828282'
    BODY_HEX = '#dddddd'
    FOOTER_HEX = '#828282'
    TITLE_HEX = '#dedede'
    BIG_SCORE_HEX = '#646464'
    IMG_COLOR = '#222222'

    TITLE_FOOTER = str(RedditTitle.num_com) + ' comments  source  share  save  hide  give award  report  crosspost  ' \
                                            'hide all child comments'
    PARENT_FOOTER = 'permalink  source  embed  save  save-RES  report  give award  reply  hide child comments'
    CHILD_FOOTER = 'permalink  source  embed  save  save-RES  parent  report  give award  reply  hide child comments'

# Imported with moviepy
TRANSITION = VideoFileClip('Static/NewError.mp4').set_duration(.7).set_fps(VID_FPS)
OUTRO = VideoFileClip('Static/outro.mp4').set_fps(VID_FPS)
LASAGNA = AudioFileClip('Static/lasagna.wav').set_duration(.33)


def permutate_word(s):
    """
    Function:   permutate_word
    Definition: this function accepts a word and returns a list of all possible capitalizations for a given word
    Parameter:  a string
    Return:     a list of strings
    """

    return list(''.join(t) for t in itertools.product(*zip(s.lower(), s.upper())))


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


def human_time(post_datetime):
    """
    Function:   human_time
    Definition: The function accepts a given date time object and calculates the difference between the current point
                in time and the time given by the parameter.
                The function then returns a roughly accurate human readable representation of the time difference
    Parameter:  a datetime object ( time posted )
    Return:     a string
    """
    dif = datetime.datetime.now() - post_datetime + datetime.timedelta(hours=8)
    seconds = dif.total_seconds()
    minutes = seconds / 60
    hours = minutes / 60
    if int(hours) < 1:
        return str(int(minutes)) + ' minutes ago'
    elif int(hours) == 1:
        return 'an hour ago'

    days = hours / 24
    if int(days) < 1:
        return str(int(hours)) + ' hours ago'
    elif int(days) == 1:
        return '1 day ago'

    weeks = days / 7
    if int(weeks) < 1:
        return str(int(days)) + ' days ago'
    elif int(weeks) == 1:
        return 'a week ago'

    months = days / 30
    if int(months) < 1:
        return 'over a week ago'
    elif int(months) == 1:
        return 'a month ago'

    years = months / 12
    if int(years) < 1:
        return str(int(months)) + ' months ago'
    elif int(years) == 1:
        return 'a year ago'
    else:
        return str(int(years)) + ' years ago'


def minute_format(num, round_to=2):
    """
    Function:   minute_format
    Definition: The function receives time in seconds which it the converts to minutes using a simple algorithm.
                The remainder is then reconverted back in to seconds and rounds to what ever number is needed
                After, seconds and minutes are formatted according to their value
    Parameter:  num (seconds), round_to (decimal places to round to)
    Return:     a string
    """
    minutes = int(abs(num) / 60)
    seconds = round(abs(num) % 60, round_to)

    if num < 0:         # in the case that the number is negative
        minutes = '-' + str(minutes)
    if seconds < 10:
        seconds = '0' + str(seconds)
    return str(minutes) + ':' + str(seconds)


def abbreviate_number(num, use_at=1000):
    """
    Function:   abbreviate_number
    Definition: This function takes a given number as shortens it.
                eg. 1000000 becomes 1M, and 1000 becomes 1k
    Parameter:  num
    Return:     an abbreviated string of the original number
    """
    if num >= use_at:
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '%.1f%s' % (num, ['', 'k', 'M', 'G', 'T', 'P'][magnitude])  # suffixes
    else:
        return str(num)


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
    if (comment_list[index].string != DNE) and (comment_list[index].score >= MIN_SCORE):
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
    if (reply_list[index].string != DNE) and (reply_list[index].score >= threshold * comment_list[index].score):
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
    if use_reply(comment) and (rtr_list[index].string != DNE) and (
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
            temp_com = replace_me(submission.comments[i].body, all_rep, all_rep_with)
            temp_com = re.sub(r"\[(.+)\]\(.+\)", r"\1", temp_com)
        except:
            temp_com = DNE

        # Creates the authors if they exist
        if submission.comments[i].stickied:
            temp_com = DNE
        if temp_com != DNE:
            try:
                temp_name = submission.comments[i].author.name  # and indexes them starting at 0
            except:
                temp_name = '[deleted]'

            temp_score = submission.comments[i].score
            temp_time = human_time(datetime.datetime.fromtimestamp(submission.comments[i].created))
            temp_gildings = submission.comments[i].gildings
        else:
            temp_name = DNE
            temp_score = DNE
            temp_time = DNE
            temp_gildings = DNE

        comment_list.append(RedditItem(temp_com, temp_name, temp_score, temp_time, temp_gildings))
        str_comment_list.append(comment_list[i].string)
        # print(temp_gildings)
        del temp_com
        del temp_name
        del temp_score
        del temp_time
        del temp_gildings

    for i in range(number_comments):  # gets all all comments saves them to a string

        # Creates the comments if they exist
        try:
            temp_com = replace_me(submission.comments[i].replies[0].body, all_rep, all_rep_with)
            temp_com = re.sub(r"\[(.+)\]\(.+\)", r"\1", temp_com)
        except:
            temp_com = DNE

        # Creates the authors if they exist
        if temp_com != DNE:
            try:
                temp_name = submission.comments[i].replies[0].author.name  # and indexes them starting at 0
            except:
                temp_name = '[deleted]'
            temp_score = submission.comments[i].replies[0].score
            temp_time = human_time(datetime.datetime.fromtimestamp(submission.comments[i].replies[0].created))
            temp_gildings = submission.comments[i].replies[0].gildings

        else:
            temp_name = DNE
            temp_score = DNE
            temp_time = DNE
            temp_gildings = DNE

        reply_list.append(RedditItem(temp_com, temp_name, temp_score, temp_time, temp_gildings))

        del temp_com
        del temp_name
        del temp_score
        del temp_time
        del temp_gildings

    for i in range(number_comments):  # gets all all comments saves them to a string

        # Creates the comments if they exist
        try:
            temp_com = replace_me(submission.comments[i].replies[0].replies[0].body, all_rep, all_rep_with)
            temp_com = re.sub(r"\[(.+)\]\(.+\)", r"\1", temp_com)
        except:
            temp_com = DNE

        # Creates the authors if they exist and indexes them starting at 0
        if temp_com != DNE:
            try:
                temp_name = submission.comments[i].replies[0].replies[0].author.name
            except:
                temp_name = '[deleted]'
            temp_score = submission.comments[i].replies[0].replies[0].score
            temp_time = human_time(
                datetime.datetime.fromtimestamp(submission.comments[i].replies[0].replies[0].created))
            temp_gildings = submission.comments[i].replies[0].replies[0].gildings
        else:
            temp_name = DNE
            temp_score = DNE
            temp_time = DNE
            temp_gildings = DNE

        rtr_list.append(RedditItem(temp_com, temp_name, temp_score, temp_time, temp_gildings))

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
    body_font = ImageFont.truetype(BODY_FONT_DIR, 20)
    author_font = ImageFont.truetype(AUTHOR_FONT_DIR, alt_font_size)
    time_font = ImageFont.truetype(TIME_FONT_DIR, alt_font_size)
    footer_font = ImageFont.truetype(FOOTER_FONT_DIR, redesign_footer_font)

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

    img = Image.new('RGBA', (image_width, img_height), IMG_COLOR)
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
        formatted_points = f'  {str(abbreviate_number(scr, 10000))} points  '
        prev_indent = indent
        indent += 40

        if num > 0:
            line_height += large_space

            fttr = CHILD_FOOTER
        else:
            fttr = PARENT_FOOTER

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

        draw.text((auth_x, auth_y), auth, font=author_font, fill=AUTHOR_HEX)
        draw.text((scr_x, scr_y), formatted_points, font=author_font, fill=SCORE_HEX)
        draw.text((tm_x, tm_y), formatted_time, font=time_font, fill=FOOTER_HEX)

        img.paste(COMMENT_VOTE_ICON, (arrow_indent, line_height), COMMENT_VOTE_ICON)
        img.paste(gld_icon, (gld_x, gld_y), gld_icon)

        for string in fmt_com:
            line_height += line_spacing
            string_num = fmt_com.index(string)
            draw.text((indent, line_height), string, font=body_font, fill=BODY_HEX)
            img_path = IMG_DIR + str(index) + '.' + str(num) + '.' + str(string_num) + '.png'

            if string == fmt_com[-1]:
                line_height += medium_space
                draw.text((indent, line_height), fttr, font=footer_font, fill=FOOTER_HEX)

            temp = BACKGROUND.copy()
            temp.paste(img, (0, 540 - int(.5 * img_h)), img)
            temp.save(img_path)

        num += 1

    comment_img(formatted_comment, author, score, com_time, gld_icon)
    if use_reply(comment):
        comment_img(formatted_reply, rep_author, rep_score, rep_time, rep_gld_icon)
    if use_rtr(comment):
        comment_img(formatted_rtr, rtr_author, rtr_score, rtr_time, rtr_gld_icon)

    photofilepath = IMG_DIR + str(index) + '.png'
    # img.show()


def create_txt(comment):
    """
    Function:   create_txt
    Definition: This function takes our gathered text and saves them to a file so that the text can be read by balcon
    Parameter:  Reddit Item
    Return:     NONE
    """
    index = str_comment_list.index(comment)

    filename = TXT_DIR + str(index) + '.0.txt'
    txt_to_save = open(filename, 'w', encoding='utf-8')
    txt_to_save.write(replace_me(comment, aud_rep, aud_rep_with, use_for_audio=True))
    txt_to_save.close()
    if use_reply(comment):
        filename = TXT_DIR + str(index) + '.1.txt'
        txt_to_save = open(filename, 'w', encoding='utf-8')  # for some reason as of 6/17/19 1:10 AM IT NEEDS ENCODING
        txt_to_save.write(replace_me(reply_list[index].string, aud_rep, aud_rep_with, use_for_audio=True))
        txt_to_save.close()
    else:
        pass

    if use_rtr(comment):
        filename = TXT_DIR + str(index) + '.2.txt'
        txt_to_save = open(filename, 'w', encoding='utf-8')  # for some reason as of 6/17/19 1:10 AM IT NEEDS ENCODING
        txt_to_save.write(replace_me(rtr_list[index].string, aud_rep, aud_rep_with, use_for_audio=True))
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
        command = f'balcon -f "Subs\\Sub1\\Txt\\{txt_file}" -w "Subs\\Sub1\\Wav\\{wav_file}" -n "ScanSoft Daniel_Full_22kHz"'
        os.system(command)
        # print(command)

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
    Function:
    Definition:
    Parameter:
    Return:
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

    a0_path = WAV_DIR + str(index) + '.0.wav'
    a1_path = WAV_DIR + str(index) + '.1.wav'
    a2_path = WAV_DIR + str(index) + '.2.wav'

    sum0 = sum(len(zero) for zero in split_com)
    sum1 = sum(len(one) for one in split_rep)
    sum2 = sum(len(two) for two in split_rtr)

    a_clip0 = AudioFileClip(a0_path)
    a_clip0 = concatenate_audioclips([a_clip0, LASAGNA])
    for string in split_com:
        factor = len(string) / sum0
        path = IMG_DIR + str(index) + '.0' + '.%s.png' % split_com.index(string)
        clip = ImageClip(path).set_duration(factor * a_clip0.duration)
        i_clip0.append(clip)
        # print(path)

    s0 = '\ndone comment: ' + str(index)
    i_clip0 = concatenate_videoclips(i_clip0)
    i_clip0 = i_clip0.set_audio(a_clip0)
    c_clip.append(i_clip0)

    if use_reply(comment):
        a_clip1 = AudioFileClip(a1_path)
        a_clip1 = concatenate_audioclips([a_clip1, LASAGNA])
        for rString in split_rep:
            factor = len(rString) / sum1
            path = IMG_DIR + str(index) + '.1' + '.%s.png' % split_rep.index(rString)
            clip = ImageClip(path).set_duration(factor * a_clip1.duration)
            i_clip1.append(clip)
            # print(path)

        s1 = '\n\tdone reply: ' + str(index)
        i_clip1 = concatenate_videoclips(i_clip1)
        i_clip1 = i_clip1.set_audio(a_clip1)
        c_clip.append(i_clip1)
    else:
        s1 = ''
        pass

    if use_rtr(comment):
        a_clip2 = AudioFileClip(a2_path)
        a_clip2 = concatenate_audioclips([a_clip2, LASAGNA])
        for rtrString in split_rtr:
            factor = len(rtrString) / sum2
            path = IMG_DIR + str(index) + '.2' + '.%s.png' % split_rtr.index(rtrString)
            clip = ImageClip(path).set_duration(factor * a_clip2.duration)
            i_clip2.append(clip)
            # print(path)
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


def replace_me(string, to_replace, replace_with, use_for_audio=False):
    """
    Function:
    Definition:
    Parameter:
    Return:
    """
    if len(to_replace) != len(replace_with):
        print("Error in replace_me")
        sys.exit()
    for item1, item2 in zip(to_replace, replace_with):
        string = string.replace(item1, item2)
    if use_for_audio:
        if RedditTitle.subreddit == 'relationships' or 'relationship_advice':
            # string = re.sub(r'[\(\[]?[0-9]+[FfMm][\)\]]? ', r'\0', string)
            pass

    return string


def create_sub():
    """
    Function:   create_sub
    Definition: This funtion combines all steps prevoisly done
                The function creates an image for the submission, converts the body text of the post to audio,
                then, the program creates a clip from the photo and audio
    Parameter:  NONE
    Return:     NONE
    """
    size = 20
    width = 180
    subreddit = str(RedditTitle.subreddit)
    body_nolinks = re.sub(r"\[(.+)\]\(.+\)", r"\1", RedditTitle.body)
    body_nolinks = re.sub(r'https?:\/\/.*[\r\n]*', '', body_nolinks)
    body_nolinks = replace_me(body_nolinks, all_rep, all_rep_with)

    author_font = ImageFont.truetype(AUTHOR_FONT_DIR, 15)
    score_font = ImageFont.truetype(SCORE_FONT_DIR, size - 3)
    title_font = ImageFont.truetype(TITLE_FONT_DIR, size)
    body_font = ImageFont.truetype(BODY_FONT_DIR, size - 2)
    sub_font = ImageFont.truetype(SUB_FONT_DIR, size - 6)
    footer_font = ImageFont.truetype(FOOTER_FONT_DIR, size - 6)

    formatted_title = textwrap.wrap(RedditTitle.title, width=width)
    formatted_body = textwrap.wrap(body_nolinks, width=width + 8)
    post_date_by = 'submitted ' + human_time(RedditTitle.created) + ' by '

    formatted_points = str(abbreviate_number(RedditTitle.score)).replace('.0', '')

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

    sub_img = Image.new('RGBA', (1920, sub_height), IMG_COLOR)  # from #222222
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
    sub_img.paste(SUB_SCORE_ICON, (15, line_height + 2), SUB_SCORE_ICON)
    sub_draw.text((indent, line_height + 26), formatted_points, font=score_font, fill=BIG_SCORE_HEX)

    # Writes each line in the title
    for line in formatted_title:
        sub_draw.text((indent_spacing, line_height), line, font=title_font, fill=TITLE_HEX)
        if line == formatted_title[-1]:
            the_sizex, the_sizey = title_font.getsize(formatted_title[-1])
            sub_draw.text((indent_spacing + the_sizex + 5, line_height + 5), f'(self.{str(RedditTitle.subreddit)})',
                          font=sub_font, fill='#888888')
        line_height = line_height + line_spacing
    del line

    # Adds spacing then writes the post date and author
    line_height += small_space
    sub_draw.text((indent_spacing, line_height), post_date_by, font=author_font, fill=TIME_HEX)
    rrx, rry = author_font.getsize(post_date_by)
    sub_draw.text((indent_spacing + rrx, line_height), ' ' + str(RedditTitle.author), font=author_font, fill=AUTHOR_HEX)
    line_height += small_space

    temp = BACKGROUND.copy()

    filename = TXT_DIR + 'title.txt'
    with open(filename, 'w', encoding='utf-8') as title_txt:  # for some reason as of 6/17/19 1:10 AM IT NEEDS ENCODING
        title_txt.write(replace_me(RedditTitle.title, aud_rep, aud_rep_with, use_for_audio=True))
    print(subreddit)

    formatted_sub = subreddit.replace('_', ' ').replace('AmItheAsshole', 'Am I The Asshole')
    formatted_sub = re.sub(r"(\w)([A-Z])", r"\1 \2", formatted_sub)
    formatted_sub = f'r/ {formatted_sub}'

    with open(TXT_DIR + 'sub_text.txt', 'w', encoding='utf-8') as sub_txt:
        sub_txt.write(formatted_sub)

    os.chdir(BALCON_DIR)  # changes command line directory for the balcon utility
    txt_file = 'title.txt'
    wav_file = 'title.wav'
    balcom = f'balcon -f "Subs\\Sub1\\Txt\\{txt_file}" -w "Subs\\Sub1\\Wav\\{wav_file}" -n "ScanSoft Daniel_Full_22kHz"'
    os.system(balcom)
    while not os.path.isfile(WAV_DIR + 'title.wav'):
        time.sleep(.12)

    os.chdir(BALCON_DIR)  # changes command line directory for the balcon utility
    txt_file = 'sub_text.txt'
    wav_file = 'sub_text.wav'
    balcom = f'balcon -f "Subs\\Sub1\\Txt\\{txt_file}" -w "Subs\\Sub1\\Wav\\{wav_file}" -n "ScanSoft Daniel_Full_22kHz"'
    os.system(balcom)
    while not os.path.isfile(WAV_DIR + 'sub_text.wav'):
        time.sleep(.12)

    sub_aclip = AudioFileClip(WAV_DIR + 'sub_text.wav')
    title_aclip = AudioFileClip(WAV_DIR + 'title.wav')
    title_aclip = concatenate_audioclips([sub_aclip, LASAGNA, title_aclip, LASAGNA])

    if RedditTitle.body != '':
        # Draws a rectangle at line spacing + large space
        # large_space - small_space is used to negate the previous addition to line height
        len_body = len(formatted_body)
        line_height += large_space
        sub_draw.rectangle([indent_spacing, line_height - medium_space, 1920 - 100, small_space + line_height +
                            len_body * line_spacing], fill=None, outline='#cccccc', width=1)

        body_iclips = []

        filename = TXT_DIR + 'body.txt'
        body_txt_file = open(filename, 'w',
                              encoding='utf-8')  # for some reason as of 6/17/19 1:10 AM IT NEEDS ENCODING
        body_txt_file.write(replace_me(body_nolinks, aud_rep, aud_rep_with, use_for_audio=True))
        body_txt_file.close()

        os.chdir(BALCON_DIR)  # changes command line directory for the balcon utility
        txt_file = 'body.txt'
        wav_file = 'body.wav'
        balcom = f'balcon -f "Subs\\Sub1\\Txt\\{txt_file}" -w "Subs\\Sub1\\Wav\\{wav_file}" -n "ScanSoft Daniel_Full_22kHz"'
        os.system(balcom)
        while not os.path.isfile(WAV_DIR + 'body.wav'):
            time.sleep(.12)
        body_aclip = AudioFileClip(WAV_DIR + 'body.wav')

        sum_body = sum(len(fff) for fff in formatted_body)

        temp.paste(sub_img, (0, 540 - int(.5 * sub_height)), sub_img)
        temp.save(IMG_DIR + 'title.png')
        title_vclip = ImageClip(IMG_DIR + 'title.png').set_audio(title_aclip).set_duration(title_aclip.duration)

        # Creates Text Body
        for line in formatted_body:
            index = formatted_body.index(line)
            sub_draw.text((indent_spacing + 10, line_height), line, font=body_font, fill='#dddddd')
            line_height = line_height + line_spacing

            if line == formatted_body[-1]:
                line_height += medium_space
                sub_draw.text((indent_spacing, line_height), TITLE_FOOTER, font=footer_font, fill=FOOTER_HEX)
            temp.paste(sub_img, (0, 540 - int(.5 * sub_height)), sub_img)

            temp.save(IMG_DIR + f'body.{index}.png')

            factor = len(line)/sum_body
            print(str(factor))
            body_iclips.append(ImageClip(IMG_DIR + f'body.{index}.png').set_duration(factor * body_aclip.duration))
        del line

        body_iclip = concatenate_videoclips(body_iclips)
        body_vclip = body_iclip.set_audio(body_aclip)
        body_vclip = concatenate_videoclips([title_vclip, body_vclip, TRANSITION])

        return body_vclip
    else:
        # Places Space Then Draws Footer
        line_height += medium_space + more_spacing
        sub_draw.text((indent_spacing, line_height), TITLE_FOOTER, font=footer_font, fill=FOOTER_HEX)

        temp.paste(sub_img, (0, 540 - int(.5 * sub_height)), sub_img)
        temp.save(IMG_DIR + 'title.png')

        title_iclip = ImageClip(IMG_DIR + 'title.png').set_duration(title_aclip.duration)
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
    shutil.rmtree(IMG_DIR)
    print('Removed IMG')
    time.sleep(.05)
    os.mkdir(IMG_DIR)
    print("Created IMG")

    shutil.rmtree(TXT_DIR)
    print('Removed TXT')
    time.sleep(.05)
    os.mkdir(TXT_DIR)
    print('Created TXT')

    shutil.rmtree(WAV_DIR)
    print('Removed WAV')
    time.sleep(.05)
    os.mkdir(WAV_DIR)
    print('Created WAV')

    if os.path.isfile('Upload/Final.mp4'):
        os.remove('Upload/Final.mp4')
        print('Removed Vid Copy')
    if os.path.isfile('Upload/thumb.png'):
        os.remove('Upload/thumb.png')
        print('Removed Thumb Copy')
    if not os.path.isdir(VID_DIR):
        os.mkdir(VID_DIR)
        print("VID DNE ... Making VID")
    if del_vid and os.path.isdir(VID_DIR):
        shutil.rmtree(VID_DIR)
        print('Removed VID')
        time.sleep(.05)
        os.mkdir(VID_DIR)
        print("Created VID")

    del_vid = False


def create_thumbnail():
    """
    Function:   create_thumbnail
    Definition:
    Parameter:  NONE
    Return:     NONE
    """
    def color_options():
        """
        Function:   color_options
        Definition: Accepts user input for preferred background color
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
            print('Choice is not recognized reverting to defaults')
            color = '#222222'
        return color

    # date = datetime.datetime.fromtimestamp(submission.created_utc)
    # dif = datetime.datetime.utcnow() - date
    # print(dif)

    sub_time = RedditTitle.created
    subreddit = 'r/' + str(RedditTitle.subreddit)
    author = 'u/' + str(RedditTitle.author)
    score = int(RedditTitle.score)
    num_com = int(RedditTitle.num_com)
    title = RedditTitle.title.replace('/', ' ').replace('[', '').replace(']', '')
    if cust_title != '0':
        title = cust_title
    thumbnail = Image.new('RGBA', (1920, 1080), color_options())  # from #222222
    thumb_draw = ImageDraw.Draw(thumbnail)
    width = 31
    formatted_title = textwrap.wrap(title, width=width)

    icon_w, icon_h = ASKREDDIT_ICON.size

    size = 90
    sub_font = ImageFont.truetype('CustFont/NimbusSanL-Reg.ttf', 75)
    author_font = ImageFont.truetype('CustFont/NimbusSanL-Bol.ttf', 45)
    score_font = ImageFont.truetype('CustFont/NimbusSanL-Bol.ttf', 60)

    base_height = 210
    line_spacing = 90
    indent_spacing = 40
    point_x, point_y = -40, 720

    # thumbnail.paste(COMMENT_ICON, (300, 850), COMMENT_ICON)
    # thumbnail.paste(UPDOWNVOTE, (point_x, point_y), UPDOWNVOTE)
    thumbnail.paste(ASKREDDIT_ICON, (40, 40), ASKREDDIT_ICON)

    thumb_draw.text((icon_w + indent_spacing + 30, 120), f'submitted {human_time(sub_time)} by {author}',
                    font=author_font, fill='#818384')

    thumb_draw.text((icon_w + indent_spacing + 30, 40), subreddit, font=sub_font)
    # thumb_draw.text((90, 910), str(abbreviate_number(score)), font=score_font, fill='#FF8C60')
    # thumb_draw.text((500, 900), str(abbreviate_number(num_com)) + '  Comments', font=score_font, fill='#818384')

    line_height_thumb = base_height
    # print(str(len(formatted_title) * (size + line_spacing)))
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
    # print(str(len(formatted_title) * (size + line_spacing)))
    # print(count_1, count_2)
    for line in formatted_title:
        body_font = ImageFont.truetype('CustFont/American_Captain.ttf', size)

        draw_outlined_text(indent_spacing, line_height_thumb, thumb_draw, body_font, line, width=3)

        line_height_thumb = line_height_thumb + line_spacing

    # thumbnail.show()
    thumbnail.save(VID_DIR + 'thumb.png')

    # draw.text((indent, com_img_height - 25), footer_parent, font=author_font, fill="#828282")
    # img.paste(commentUpDownIcon, (arrow_indent, 13), commentUpDownIcon)


def data_collection():
    """
    Function:   data_collection
    Definition: Appends all function data to a csv file
    Parameter:  NONE
    Return:     NONE
    """
    csv_row = [str(charSum), str(final.duration), str(number_comments), str(threshold), str(datetime.datetime.now()),
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
               '\nTimestamp: ' + minute_format(dur_counter - song_sound[index].duration, 0) + \
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


def estimate_time():
    """
    Function:   estimate_time
    Definition: Adds up the total number of characters in the entirity of the video and comes up with a time
                estimate in seconds.
    Parameter:  NONE
    Return:     NONE
    """
    global estimated_time
    global charSum
    charSum = len(str(RedditTitle.title)) + len(RedditTitle.body)
    for x in str_comment_list[:number_comments]:
        gh = str_comment_list.index(x)
        charSum = charSum + len(x)
        if use_reply(x):
            charSum = charSum + len(reply_list[gh].string)
        else:
            pass
        if use_rtr(x):
            charSum = charSum + len(rtr_list[gh].string)
        else:
            pass

    estimated_time = reg.predict([[charSum, number_comments, threshold]])[0]
    estimated_time = round(estimated_time, 5)


def video_creation(comment):
    """
    Function:   video_creation
    Definition: Thus appends clips to the clip array, the function also makes sure the files neccesaary have 
                already been created
    Parameter:  RedditItem
    Return:     NONE
    """
    index = str_comment_list.index(comment)
    create_txt(comment)
    create_wav(comment)
    create_img(comment)
    # createAudioClip(comment)
    sp0 = WAV_DIR + str(index) + '.0.wav'
    sp1 = WAV_DIR + str(index) + '.1.wav'
    sp2 = WAV_DIR + str(index) + '.2.wav'
    # print(sp0)
    # print(sp1)
    # print(sp2)
    while not os.path.isfile(sp0):
        print(sp0)
        time.sleep(.3)
        print("waiting for comment:" + str(index))
    if use_reply(comment):
        while not os.path.isfile(sp1):
            time.sleep(.3)
            print("waiting for reply:" + str(index))
    else:
        pass
    if use_rtr(comment):
        while not os.path.isfile(sp2):
            time.sleep(.3)
            print("waiting for comment:" + str(index))
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
        'title': RedditTitle.title + ' (r/AskReddit)',
        'description': f'r/{str(RedditTitle.subreddit)} Videos! Welcome back to a brand new USER video!'
                       '\n\n Dont forget to like and subscribe'
                       '\n'
                       '\n I love to upload New daily videos to keep yall entertained'
                       '\n'
                       '\n🎧♪♫ [Track List] ♫♪🎧 '
                       f'\n{sound_desc}\n'
                       '\nOutro Template made by Grabster - Youtube.com/GrabsterTV'
                       '\n'
                       f'\nSubreddits used: r/{str(RedditTitle.subreddit)}'
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
    # print(data['description'])
    with open(UPLOAD_DIR + 'data.json', 'w') as f:
        json.dump(data, f)
    with open(VID_DIR + 'description.txt', 'w', encoding='utf-8') as desc:
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
    shutil.copy2(VID_DIR + 'thumb.png', UPLOAD_DIR)
    command = []
    os.chdir(UPLOAD_DIR)
    command.append('youtubeuploader_windows_amd64 ')
    command.append('-filename ' + vid_name + vid_extension + ' ')
    command.append('-thumbnail ' + 'thumb.png ')
    command.append('-metaJSON string ' + 'data.json')
    command = ''.join(command)
    os.system(command)
    print(command)


def insensitive_replace_list(find_list, replace_list, end_of_stmt=['.', '?', '!', ',', ' ', '\n', '</?']):
    """
    Function:   insensitive_replace_list
    Definition:
    Parameter:
    Return:
    """
    for n, i in enumerate(find_list):
        find_list[n] = permutate_word(i)
    for n, i in enumerate(replace_list):
        replace_list[n] = [str(i) for j in find_list[n]]

    find_list = list(itertools.chain(*find_list))
    replace_list = list(itertools.chain(*replace_list))

    find_list = [k + end_of_stmt[end_of_stmt.index(i)] for k in find_list for i in end_of_stmt]
    replace_list = [k + end_of_stmt[end_of_stmt.index(i)] for k in replace_list for i in end_of_stmt]

    return find_list, replace_list


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
aita_1, aita_2 = insensitive_replace_list(
    ['aita', 'yta', 'nta', 'esh'],
    ['am i the asshole', 'you\'re the asshole', 'not the asshole', 'everyone sucks here']
)

# if these values are not changed the tts engine will read the arcronyms, leading to mispronunciations
sms_1, sms_2 = insensitive_replace_list(
    ['lol ', 'lol.', 'jk', 'smh', 'stfu', 'nvm', 'tbh', 'tifu'],
    ['el oh el', 'el oh el.', 'just kidding', 'shake my head', 'shut the fuck up', 'nevermind', 'to be honest', 'today i fucked up']
)

# These are words that the TTS engine often mispronounces
common_mispronunciations_1, common_mispronunciations_2 = insensitive_replace_list(
    ['coworker', 'facebook'],
    ['co-worker', 'face book']
)
# Censors swear words
swear_1, swear_2 = insensitive_replace_list(
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
estimate_time()
print(f'\nMaximum Video Length is: {minute_format(estimated_time)} or {str(estimated_time)}s')

if desired_vid_len > estimated_time:
    desired_vid_len = estimated_time
    print(f'\nInput exceeds maximum time of {estimated_time}s for this reddit post, setting time to {estimated_time}')

while estimated_time > desired_vid_len:
    number_comments -= 1
    estimate_time()
    if estimated_time <= desired_vid_len:
        break

    for y in range(5):
        threshold += .08
        estimate_time()
        if estimated_time <= desired_vid_len:
            break

    estimate_time()
    if estimated_time <= desired_vid_len:
        break
    threshold = .3

print(f'\nEstimated Video Length is: {minute_format(estimated_time)} or {str(estimated_time)}s')
print(f'Number of Comments: {number_comments}')
print(f'Threshold: {threshold}')

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
background_music = song_sound.set_duration(final.duration)
final_audio = CompositeAudioClip([final.audio, background_music])
final = final.set_audio(final_audio)

# Used to compare the estimated video length the the actual length
pct_diff = round(100 - (abs(estimated_time / final.duration) * 100), 2)
if pct_diff > 0:
    pct_diff = '+' + str(pct_diff)
else:
    pct_diff = str(pct_diff)
abs_diff = final.duration - estimated_time
formatted_diff = minute_format(abs_diff)
if float(abs_diff) > 0:
    formatted_diff = '+' + formatted_diff
else:
    pass

print(f'\n \nActual Video Length is: {minute_format(final.duration)} / {str(final.duration)}s. '
      f'Shifted {formatted_diff} / {str(pct_diff)}% from {minute_format(estimated_time)} / {str(estimated_time)}s\n')

vid_name = str(submission.id)
vid_extension = '.mp4'
video_path = VID_DIR + vid_name + vid_extension
final.write_videofile(video_path, fps=VID_FPS, threads=16, preset='ultrafast')

metadata()
# upload_video()

# Collects data to help improve the program's predictions
data_collection()
print('\n')
cleanup()

print('\nClosing in 10 seconds')
time.sleep(10)