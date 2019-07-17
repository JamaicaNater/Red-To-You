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


class RedditItem(object):
    def __init__(self, string, author, score):
        self.string = string
        self.author = author
        self.score = score

    def split_self(self, width):
        split = textwrap.wrap(self.string, width=width)
        return split

    def get_split_len(self, width):
        split_len = textwrap.wrap(self.string, width=width)
        return len(split_len)


reddit = praw.Reddit(client_id='BHUtkEY0x4vomA', client_secret='MZvTVUs83p8wEN_Z8EU8bIUjGTY',
                     user_agent='pulling posts')
reddit_link = 'https://www.reddit.com/r/AskReddit/comments/ce54ei/what_did_you_think_was_your_fetish_until_you/'  # input('Paste the url leave one space then press enter\n')
submission = reddit.submission(url=reddit_link)


class RedditTitle:
    title = submission.title
    body = submission.selftext
    author = submission.author
    subreddit = submission.subreddit
    score = submission.score
    created = datetime.datetime.fromtimestamp(submission.created)
    num_com = submission.num_comments
    sub_time = datetime.datetime.now() - created + datetime.timedelta(hours=8)
    try:
        author = submission.author.name
    except:
        author = '[–] ' + '[deleted]'

    def split_self(self, width):
        split = textwrap.wrap(self.title, width=width)
        return split


number_comments = 25  # int(input('Type a Number Between 1 and 25 to represent the Number of Comments\n'))
threshold = .3  # float(input('Type a number between 0 and 1 to represent the reply threshold (.33 recommended) \n'))
MIN_SCORE = 50
DNE = 'Does Not Exist'

clip_array = []
item_list = []
comment_list = []
str_comment_list = []
reply_list = []
rtr_list = []

# Keep static, folders deleted on exit
IMG_DIR = 'Subs/Sub1/Img/'
WAV_DIR = 'Subs/Sub1/Wav/'
TXT_DIR = 'Subs/Sub1/Txt/'
VID_DIR = 'Subs/Vid/'

# EXE Directories
BALCON_DIR = os.path.dirname(os.path.abspath("balcon.exe"))
UPLOAD_DIR = os.path.dirname(os.path.abspath('Upload/youtubeuploader_windows_amd64.exe')) + '\\'

vid_name = 'Final'
vid_extension = '.mp4'
video_path = VID_DIR + vid_name + vid_extension

cWidth = 175
rWidth = 168
rtrWidth = 161
VidFPS = 15

# Imported with Pillow
BACKGROUND = Image.open('Static/backgroundblack.jpg').convert('RGBA')
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

# Lists all the hex code for fill
AUTHOR_HEX = '#6a98af'
SCORE_HEX = '#b4b4b4'
TIME_HEX = '#828282'
BODY_HEX = '#dddddd'
FOOTER_HEX = '#828282'
TITLE_HEX = '#dedede'
BIG_SCORE_HEX = '#646464'

# Imported with moviepy
TRANSITION = VideoFileClip('Static/NewError.mp4').set_duration(.7).set_fps(VidFPS)
OUTRO = VideoFileClip('Static/outro.mp4').set_fps(VidFPS)


def cc(s):
    return list(''.join(t) for t in itertools.product(*zip(s.lower(), s.upper())))


def human_time(reddit_time):
    seconds = reddit_time.total_seconds()
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
    minutes = int(abs(num) / 60)
    seconds = round(abs(num) % 60, round_to)
    if num < 0:
        minutes = '-' + str(minutes)
    if round_to == 0:
        seconds = int(seconds)
    if seconds < 10:
        seconds = '0' + str(seconds)
    return str(minutes) + ':' + str(seconds)


def human_format(num, use_at=1000):
    if num >= use_at:
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        # add more suffixes if you need them
        return '%.1f%s' % (num, ['', 'k', 'M', 'G', 'T', 'P'][magnitude])
    else:
        return num


def bool_comment(comment):
    index = str_comment_list.index(comment)
    if (comment_list[index].string != DNE) and (comment_list[index].score >= MIN_SCORE):
        if index == 0:
            return not submission.comments[0].stickied
        else:
            return True
    else:
        return False


def bool_reply(comment):
    index = str_comment_list.index(comment)
    if (reply_list[index].string != DNE) and (comment_list[index].score >= threshold * reply_list[index].score):
        return True
    else:
        return False


def bool_rtr(comment):
    index = str_comment_list.index(comment)
    if bool_reply(comment) and (rtr_list[index].string != DNE) and (rtr_list[index].score >= reply_list[index].score * threshold):
        return True
    else:
        return False


def fill_comment_items():
    for i in range(number_comments):  # gets all all comments saves them to a string
        # Creates the comments if they exist
        try:
            temp_com = replace_me(submission.comments[i].body, all_rep, all_rep_with)
            temp_com = re.sub(r"\[(.+)\]\(.+\)", r"\1", temp_com)
        except:
            temp_com = ('[–] ' + '[deleted]')

        # Creates the authors if they exist
        try:
            temp_name = ('[–] ' + submission.comments[i].author.name)  # and indexes them starting at 0
        except:
            temp_name = ('[–] ' + '[deleted]')

        temp_score = submission.comments[i].score

        comment_list.append(RedditItem(temp_com, temp_name, temp_score))
        str_comment_list.append(comment_list[i].string)
        del temp_com
        del temp_name
        del temp_score


def fill_reply_items():
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
                temp_name = ('[–] ' + submission.comments[i].replies[0].author.name)  # and indexes them starting at 0
            except:
                temp_name = ('[–] ' + '[deleted]')
        else:
            temp_name = DNE

        try:
            temp_score = submission.comments[i].replies[0].score
        except:
            temp_score = DNE
        reply_list.append(RedditItem(temp_com, temp_name, temp_score))
        del temp_com
        del temp_name
        del temp_score


def fill_rtr_items():
    for i in range(number_comments):  # gets all all comments saves them to a string

        # Creates the comments if they exist
        try:
            temp_com = replace_me(submission.comments[i].replies[0].replies[0].body, all_rep, all_rep_with)
            temp_com = re.sub(r"\[(.+)\]\(.+\)", r"\1", temp_com)
        except:
            temp_com = DNE

        # Creates the authors if they exist
        if temp_com != DNE:
            try:
                temp_name = ('[–] ' + submission.comments[i].replies[0].replies[0].author.name)  # and indexes them starting at 0
            except:
                temp_name = ('[–] ' + '[deleted]')
        else:
            temp_name = DNE

        try:
            temp_score = submission.comments[i].replies[0].replies[0].score
        except:
            temp_score = DNE

        rtr_list.append(RedditItem(temp_com, temp_name, temp_score))
        del temp_com
        del temp_name
        del temp_score


def create_img(comment):
    index = str_comment_list.index(comment)                     # add text wrapping to string
    formatted_comment = comment_list[index].split_self(cWidth)        # text values are separated into lines,
    com_len = len(formatted_comment)                               # this gets the total number of lines
    # print(comment_list[index].string)

    # Useful Variables
    line_height = 5
    # Line height and indent are shifted dynamically in the program for simplicity
    line_spacing = 25
    medium_space = 30   # Primarily used to separate footer
    large_space = 40    # Primarily used to separate comments

    image_width = 1920
    indent = 40
    arrow_indent = indent - 30  # Arrow indend refers to the vote arrow's indentation
    footer_parent = 'permalink  source  embed  save  save-RES  report  give award  reply  hide child comments'
    footer_child = 'permalink  source  embed  save  save-RES  parent  report  give award  reply  hide child comments'
    author = comment_list[index].author

    # Fonts used in this function
    body_font = ImageFont.truetype('CustFont/Verdana.ttf', 20)
    author_font = ImageFont.truetype('CustFont/verdanab.ttf', 15)

    if bool_reply(comment):
        formatted_reply = reply_list[index].split_self(rWidth)
        rep_len = len(formatted_reply)
        rep_height = large_space + line_spacing * rep_len + medium_space
        rep_score = reply_list[index].score
        rep_author = reply_list[index].author

        def reply():
            nonlocal line_spacing
            nonlocal line_height
            nonlocal indent

            line_height += large_space
            indent += 40
            rep_w, rep_h = author_font.getsize(rep_author)
            rep_auth_x, rep_auth_y = (indent, line_height)
            rep_score_x, rep_score_y = (rep_w + indent, line_height)

            draw.text((rep_auth_x, rep_auth_y), rep_author, font=author_font, fill=AUTHOR_HEX)
            draw.text((rep_score_x, rep_score_y), f'  {str(rep_score)} points', font=author_font, fill=SCORE_HEX)

            img.paste(COMMENT_VOTE_ICON, (indent - 30, line_height), COMMENT_VOTE_ICON)
            draw.line((indent-40, img_height - 5, indent-40, rep_auth_y), fill="#B4B4B4", width=3)

            for rep_string in formatted_reply:
                line_height += line_spacing
                rep_str_num = formatted_reply.index(rep_string)
                draw.text((indent, line_height), rep_string, font=body_font, fill=BODY_HEX)
                img_path = IMG_DIR + str(index) + '.' + str(1) + '.' + str(rep_str_num) + '.png'

                if rep_string == formatted_reply[-1]:
                    line_height += medium_space
                    draw.text((indent, line_height), footer_child, font=author_font, fill=FOOTER_HEX)

                temp = BACKGROUND.copy()
                temp.paste(img, (0, 540 - int(.5 * img_h)), img)
                temp.save(img_path)

    else:
        rep_height = 0

        def reply():
            pass

    if bool_rtr(comment):
        formatted_rtr = rtr_list[index].split_self(rtrWidth)
        rtr_len = len(formatted_rtr)
        rtr_height = large_space + line_spacing * rtr_len + medium_space
        rtr_score = rtr_list[index].score
        rtr_author = rtr_list[index].author

        def rtr():
            nonlocal line_spacing
            nonlocal line_height
            nonlocal indent

            line_height += large_space
            indent += 40
            rtr_auth_w, rtr_auth_h = author_font.getsize(rtr_author)
            rtr_auth_x, rtr_auth_y = (indent, line_height)
            rtr_score_x, rtr_score_y = (rtr_auth_w + indent, line_height)

            draw.text((rtr_auth_x, rtr_auth_y), rtr_author, font=author_font,  fill=AUTHOR_HEX)
            draw.text((rtr_score_x, rtr_score_y), f'  {str(rtr_score)}  points', font=author_font, fill=SCORE_HEX)
            img.paste(COMMENT_VOTE_ICON, (indent - 30, line_height), COMMENT_VOTE_ICON)
            draw.line((indent-40, img_height - 5, indent-40, rtr_auth_y), fill="#B4B4B4", width=3)

            for rtrString in formatted_rtr:
                line_height += line_spacing
                rtr_str_num = formatted_rtr.index(rtrString)
                draw.text((indent, line_height), rtrString, font=body_font, fill=BODY_HEX)
                if rtrString == formatted_rtr[-1]:
                    line_height += medium_space
                    draw.text((indent, line_height), footer_child, font=author_font, fill=FOOTER_HEX)
                IMGPath = IMG_DIR + str(index) + '.' + str(2) + '.' + str(rtr_str_num) + '.png'
                temp = BACKGROUND.copy()
                temp.paste(img, (0, 540 - int(.5 * img_h)), img)
                temp.save(IMGPath)

    else:
        rtr_height = 0

        def rtr():
            pass

    # Potential comment height; this makes and educated guess at the comments size
    ptnl_com_height = line_height + line_spacing*com_len + medium_space
    img_height = ptnl_com_height + rep_height + rtr_height + medium_space

    img = Image.new('RGBA', (image_width, img_height), '#222222')
    draw = ImageDraw.Draw(img)

    # Gets size of several objects for later use
    img_w, img_h = img.size
    auth_w, auth_h = author_font.getsize(author)
    auth_x, auth_y = (indent, line_height)
    scr_x, scr_y = (auth_w + indent, line_height)
    
    # Draws the header for the comment
    draw.text((auth_x, auth_y), author, font=author_font, fill=AUTHOR_HEX)
    draw.text((scr_x, scr_y), f'  {str(comment_list[index].score)} points', font=author_font, fill=SCORE_HEX)
    img.paste(COMMENT_VOTE_ICON, (arrow_indent, line_height), COMMENT_VOTE_ICON)
    
    for string in formatted_comment:
        line_height += line_spacing
        string_num = formatted_comment.index(string)
        draw.text((indent, line_height), string, font=body_font, fill=BODY_HEX)
        img_path = IMG_DIR + str(index) + '.' + str(0) + '.' + str(string_num) + '.png'

        temp = BACKGROUND.copy()
        temp.paste(img, (0, 540 - int(.5 * img_h)), img)
        temp.save(img_path)

    line_height += medium_space
    draw.text((indent, line_height), footer_parent, font=author_font, fill=FOOTER_HEX)

    reply()
    rtr()

    photofilepath = IMG_DIR + str(index) + '.png'
    # img.show()


def create_txt(comment):
    index = str_comment_list.index(comment)

    filename = TXT_DIR + str(index) + '.0.txt'
    txt_to_save = open(filename, 'w', encoding='utf-8')  # for some reason as of 6/17/19 1:10 AM IT NEEDS ENCODING
    txt_to_save.write(replace_me(comment, aud_rep, aud_rep_with))
    txt_to_save.close()
    if bool_reply(comment):
        filename = TXT_DIR + str(index) + '.1.txt'
        txt_to_save = open(filename, 'w', encoding='utf-8')  # for some reason as of 6/17/19 1:10 AM IT NEEDS ENCODING
        txt_to_save.write(replace_me(reply_list[index].string, aud_rep, aud_rep_with))
        txt_to_save.close()
    else:
        pass

    if bool_rtr(comment):
        filename = TXT_DIR + str(index) + '.2.txt'
        txt_to_save = open(filename, 'w', encoding='utf-8')  # for some reason as of 6/17/19 1:10 AM IT NEEDS ENCODING
        txt_to_save.write(replace_me(rtr_list[index].string, aud_rep, aud_rep_with))
        txt_to_save.close()
    else:
        pass


def create_wav(comment):
    index = str_comment_list.index(comment)

    def balcon(num):
        os.chdir(BALCON_DIR)  # changes command line directory for the balcon utility
        txt_file = str(index) + '.%s.txt' % num
        wav_file = str(index) + '.%s.wav' % num
        command = f'balcon -f "Subs\\Sub1\\Txt\\{txt_file}" -w "Subs\\Sub1\\Wav\\{wav_file}" -n "ScanSoft Daniel_Full_22kHz"'
        os.system(command)

        # print(command)
    balcon(0)
    if bool_reply(comment):
        balcon(1)
    else:
        pass
    if bool_rtr(comment):
        balcon(2)
    else:
        pass


def create_clip(comment):
    index = str_comment_list.index(comment)

    split_com = comment_list[index].split_self(cWidth)
    split_rep = reply_list[index].split_self(rWidth)
    split_rtr = rtr_list[index].split_self(rtrWidth)

    # Arrays for various clips in sequence
    c_clip = []     # Refers to comment clip ie. the whole this including replies/rtr
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
    for string in split_com:
        factor = len(string)/sum0
        path = IMG_DIR + str(index) + '.0' + '.%s.png' % split_com.index(string)
        clip = ImageClip(path).set_duration(factor * a_clip0.duration)
        i_clip0.append(clip)
        # print(path)

    s0 = '\ndone comment: ' + str(index)
    i_clip0 = concatenate_videoclips(i_clip0)
    i_clip0 = i_clip0.set_audio(a_clip0)
    c_clip.append(i_clip0)

    if bool_reply(comment):
        a_clip1 = AudioFileClip(a1_path)
        for rString in split_rep:
            factor = len(rString)/sum1
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

    if bool_rtr(comment):
        a_clip2 = AudioFileClip(a2_path)
        for rtrString in split_rtr:
            factor = len(rtrString)/sum2
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


def replace_me(string, to_replace, replace_with):
    if len(to_replace) != len(replace_with):
        CRASH
    for item1, item2 in zip(to_replace, replace_with):
        string = string.replace(item1, item2)
    return string


def create_sub():
    size = 20
    width = 180

    author_font = ImageFont.truetype('CustFont/Verdana.ttf', 15)
    score_font = ImageFont.truetype('CustFont/verdanab.ttf', size - 3)
    title_font = ImageFont.truetype('CustFont/Verdana.ttf', size)
    body_font = ImageFont.truetype('CustFont/Verdana.ttf', size - 2)
    sub_font = ImageFont.truetype('CustFont/Verdana.ttf', size - 6)
    footer_font = ImageFont.truetype('CustFont/verdanab.ttf', size - 6)

    formatted_title = textwrap.wrap(RedditTitle.title, width=width)
    formatted_body = textwrap.wrap(RedditTitle.body, width=width + 8)
    post_date_by = 'submitted ' + human_time(RedditTitle.sub_time) + ' by '
    footer = str(RedditTitle.num_com) + ' comments  source  share  save  hide  give award  report  crosspost  ' \
                                        'hide all child comments'
    formatted_points = str(human_format(RedditTitle.score)).replace('.0', '')

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

    sub_img = Image.new('RGBA', (1920, sub_height), '#222222')  # from #222222
    sub_draw = ImageDraw.Draw(sub_img)

    # Draws rectangle at current height
    sub_draw.rectangle(
        [(indent_spacing, line_height), (1920 - 10,
         15 + line_height + len(formatted_title) * line_spacing + 2 * small_space + large_space
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

    if RedditTitle.body != '':
        # Draws a rectangle at line spacing + large space
        # large_space - small_space is used to negate the previous addition to line height
        line_height += large_space
        sub_draw.rectangle([indent_spacing, line_height - medium_space, 1920 - 100, small_space + line_height +
                            len(formatted_body) * line_spacing], fill=None, outline='#cccccc', width=1)

        # Creates Text Body
        for line in formatted_body:
            sub_draw.text((indent_spacing + 10, line_height), line, font=body_font, fill='#dddddd')
            line_height = line_height + line_spacing
        del line
        more_spacing = 0

    # Places Space Then Draws Footer
    line_height += medium_space + more_spacing
    sub_draw.text((indent_spacing, line_height), footer, font=footer_font, fill=FOOTER_HEX)

    temp.paste(sub_img, (0, 540 - int(.5 * sub_height)), sub_img)

    temp.save(IMG_DIR + 'title.png')
    filename = TXT_DIR + 'title.txt'
    title_txt_file = open(filename, 'w', encoding='utf-8')  # for some reason as of 6/17/19 1:10 AM IT NEEDS ENCODING
    title_txt_file.write(replace_me(RedditTitle.title, aud_rep, aud_rep_with))
    title_txt_file.close()

    os.chdir(BALCON_DIR)  # changes command line directory for the balcon utility
    txt_file = 'title.txt'
    wav_file = 'title.wav'
    balcom = f'balcon -f "Subs\\Sub1\\Txt\\{txt_file}" -w "Subs\\Sub1\\Wav\\{wav_file}" -n "ScanSoft Daniel_Full_22kHz"'
    os.system(balcom)
    while not os.path.isfile(WAV_DIR + 'title.wav'):
        time.sleep(.12)

    title_aclip = AudioFileClip(WAV_DIR + 'title.wav')
    title_iclip = ImageClip(IMG_DIR + 'title.png').set_duration(title_aclip.duration)
    title_vclip = title_iclip.set_audio(title_aclip)
    title_vclip = concatenate_videoclips([title_vclip, TRANSITION])
    return title_vclip


def cleanup():
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


def create_thumbnail():
    def color_options():
        bgrd_choice = 2  # int(input('\nType your background color option [0 = Transparent, 1 = Default, 2 = Black]\n'))
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

    sub_time = RedditTitle.sub_time
    subreddit = 'r/' + str(RedditTitle.subreddit)
    author = 'u/' + str(RedditTitle.author)
    score = int(RedditTitle.score)
    num_com = int(RedditTitle.num_com)
    title = RedditTitle.title.replace('/', ' ')
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

    thumbnail.paste(COMMENT_ICON, (300, 850), COMMENT_ICON)
    thumbnail.paste(UPDOWNVOTE, (point_x, point_y), UPDOWNVOTE)
    thumbnail.paste(ASKREDDIT_ICON, (40, 40), ASKREDDIT_ICON)

    thumb_draw.text((icon_w + indent_spacing + 30, 120), f'submitted {human_time(sub_time)} by {author}',
                    font=author_font, fill='#818384')

    thumb_draw.text((icon_w + indent_spacing + 30, 40), subreddit, font=sub_font)
    thumb_draw.text((90, 910), str(human_format(score)), font=score_font, fill='#FF8C60')
    thumb_draw.text((500, 900), str(human_format(num_com)) + '  Comments', font=score_font, fill='#818384')

    line_height_thumb = base_height
    # print(str(len(formatted_title) * (size + line_spacing)))
    count_1 = 0
    count_2 = 0
    while not 1020 <= len(formatted_title) * (size + line_spacing) <= 1200:
        while len(formatted_title) * (size + line_spacing) >= 1200:
            count_1 = count_1 + 1
            size = size - 2
            line_spacing = line_spacing - 2
            width = width + .8
            formatted_title = textwrap.wrap(title, width=width)
            if count_1 >= 35:
                break
        while len(formatted_title) * (size + line_spacing) <= 1020:
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
        body_font = ImageFont.truetype('CustFont/NimbusSanL-Bol.ttf', size)
        thumb_draw.text((indent_spacing, line_height_thumb), line, font=body_font)
        line_height_thumb = line_height_thumb + line_spacing

    # thumbnail.show()
    thumbnail.save(VID_DIR + 'thumb.png')

    # draw.text((indent, com_img_height - 25), footer_parent, font=author_font, fill="#828282")
    # img.paste(commentUpDownIcon, (arrow_indent, 13), commentUpDownIcon)


def data_collection():
    csv_row = [str(charSum), str(final.duration), str(number_comments), str(threshold), str(datetime.datetime.now()),
               str(reddit_link)]
    with open('MLData.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(csv_row)


def dynamic_music():
    global song_sound
    global sound_desc
    song_sound = []
    song_info = []
    temp = os.path.dirname(os.path.abspath('Static/DynamicMusic/DynamicMusic.txt')) + '\\*.mp3'
    # print(temp)
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
               '\nTimestap: ' + minute_format(dur_counter - song_sound[index].duration, 0) + \
            '\n'
        song_info.append(info)

        if dur_counter > estimated_time * 1.1:
            break
    song_sound = concatenate_audioclips(song_sound)
    song_sound = song_sound.volumex(.1)
    sound_desc = ''.join(song_info)


df = pd.read_csv('MLData.csv')
reg = linear_model.LinearRegression()
reg.fit(df[['char_len', 'num_com', 'threshold']], df.duration)


def estimate_time():
    global estimated_time
    global charSum
    charSum = len(str(RedditTitle.title))
    for x in str_comment_list[:number_comments]:
        gh = str_comment_list.index(x)
        charSum = charSum + len(x)
        if bool_reply(x):
            charSum = charSum + len(reply_list[gh].string)
        else:
            pass
        if bool_rtr(x):
            charSum = charSum + len(rtr_list[gh].string)
        else:
            pass

    estimated_time = reg.predict([[charSum, number_comments, threshold]])[0]
    estimated_time = round(estimated_time, 5)
    print(f'Estimated Video Length is: {minute_format(estimated_time)} or {str(estimated_time)}s')


def video_creation(thing):
    index = str_comment_list.index(thing)
    create_txt(thing)
    create_wav(thing)
    create_img(thing)
    # createAudioClip(thing)
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
    if bool_reply(thing):
        while not os.path.isfile(sp1):
            time.sleep(.3)
            print("waiting for reply:" + str(index))
    else:
        pass
    if bool_rtr(thing):
        while not os.path.isfile(sp2):
            time.sleep(.3)
            print("waiting for comment:" + str(index))
    else:
        pass
    # time.sleep(3)
    final.append(create_clip(thing))


def metadata():
    str_tag = (
        'reddit, best of ask reddit, reddit, ask reddit top posts, r/story, r/ askreddit, r/askreddit, story time, '
        'reddify, r slash, toad films, updoot, flumpy, foxfilms, jayben, reddit & chill, bamboozled, brainydude, '
        'reddit watchers, best posts & comments, reddit sexual, reddit 2019, reddit nsfw, askreddit nsfw, Reddit Genie'
    )
    data = {
        'title': RedditTitle.title + ' (r/AskReddit)',
        'description': 'r/AskReddit Videos! Welcome back to a brand new Reddit Genie video!'
                       '\n\n🔔 Hit the bell next to Subscribe so you never miss a video!'
                       '\n🏆 Like, Comment and Subscribe if you are new on the channel!'
                       '\n👱🏻‍♂️ Comment "Reddit Genie Rulez!" if you are still reading this for a cookie!'
                       '\n'
                       '\nBest known for reddit videos, askreddit videos, text to speech videos and funny compilations.'
                       ' I upload at least one video a day to keep you all entertained! Welcome to the channel!  '
                       '\nWelcome back to a brand new video on the Reddit Genie channel where we look at new'
                       ' ask reddit funny posts and make the best funny compilations of all time. We get the best of '
                       'ask reddit and make new story time videos. Here are some of the best posts and comments! '
                       'Please like comment and subscribe. Comment your opinion down below! '
                       '\n'
                       '\n🎧♪♫ [Track List] ♫♪🎧 '
                       f'\n{sound_desc}\n'
                       '\nOutro Template made by Grabster - Youtube.com/GrabsterTV'
                       '\n'
                       f'\nSubreddits used: r/{str(RedditTitle.subreddit)}'
                       '\n'
                       '\n#relationships #reddit #askreddit #askredditscary #askredditnsfw #redditfunny #updoot '
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
    print(data['description'])
    with open(UPLOAD_DIR + 'data.json', 'w') as f:
        json.dump(data, f)


def upload_video():
    command = []
    os.chdir(UPLOAD_DIR)
    command.append('youtubeuploader_windows_amd64 ')
    command.append('-filename ' + vid_name + vid_extension + ' ')
    command.append('-thumbnail ' + 'thumb.png ')
    command.append('-metaJSON string ' + 'data.json')
    command = ''.join(command)
    os.system(command)
    print(command)


aud_rep, aud_rep_with = ['’', '‘', '”', '“', '*', ';', '^', '\\', '/', '_', 'coworker', 'Coworker', 'tbh'], \
                        ["'", "'", '"', '"', '', '', '', '', '', ' ', 'co-worker', 'co-worker', 'to be honest']
viz_rep, viz_rep_with = [], []
all_rep, all_rep_with = ['&#x200B'], ['']

lol, haha = ['LOL ', 'lol ', 'Lol ', 'LOL.', 'lol.', 'Lol.'], ['haha ', 'haha ', 'haha ', 'haha.', 'haha.', 'haha.']
emote1, emote2 = [':)', '(:', ':(', '):'], ['smiley', 'smiley', 'sad face', 'sad face']

aud_rep.extend(lol)
aud_rep_with.extend(haha)
aud_rep.extend(emote1)
aud_rep_with.extend(emote2)

del_vid = True
cleanup()
del_vid = False

create_thumbnail()
fill_comment_items()
fill_reply_items()
fill_rtr_items()

estimate_time()

tyt = 500
if tyt > estimated_time:
    tyt = estimated_time
    print(f'Input exceeds maximum time of {estimated_time}s for this comment')

while estimated_time > tyt:
    number_comments -= 1
    estimate_time()
    if estimated_time <= tyt:
        break

    for y in range(5):
        threshold += .08
        estimate_time()
        if estimated_time <= tyt:
            break

    estimate_time()
    if estimated_time <= tyt:
        break
    threshold = .1
print(number_comments)
print(threshold)

dynamic_music()

final = [create_sub()]

thread = []
for com in str_comment_list[:number_comments]:
    ind = str_comment_list.index(com)
    temp_thread = threading.Thread(target=video_creation, args=(com,))
    thread.append(temp_thread)
    thread[ind].start()
del ind
for com in str_comment_list[:number_comments]:
    ind = str_comment_list.index(com)
    thread[ind].join()
final.append(OUTRO)
del ind

final = concatenate_videoclips(final)
background_music = song_sound.set_duration(final.duration)
final_audio = CompositeAudioClip([final.audio, background_music])
final = final.set_audio(final_audio)
strong = round(100 - (abs(estimated_time/final.duration) * 100), 2)
if strong > 0:
    strong = '+' + str(strong)
else:
    strong = str(strong)
weakSauce = final.duration - estimated_time
weak = minute_format(weakSauce)
if float(weakSauce) > 0:
    weak = '+' + weak
else:
    pass

print(f'\n \nActual Video Length is: {minute_format(final.duration)} / {str(final.duration)}s. '
      f'Shifted {weak} / {str(strong)}% from {minute_format(estimated_time)} / {str(final.duration)}s')
metadata()
final.write_videofile(video_path, fps=VidFPS, threads=16, preset='ultrafast')

shutil.copy2(video_path, UPLOAD_DIR)
shutil.copy2(VID_DIR + 'thumb.png', UPLOAD_DIR)

# upload_video()
# data_collection()
cleanup()
