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

reddit_link = 'https://www.reddit.com/r/AskReddit/comments/cduruo/whats_a_mild_inconvenience_that_drives_you/'  # input('Paste the url leave one space then press enter\n')
number_comments = 25  # int(input('Type a Number Between 1 and 25 to represent the Number of Comments\n'))
threshold = .3  # float(input('Type a number between 0 and 1 to represent the reply threshold (.33 recommended) \n'))
MIN_SCORE = 50

submission = reddit.submission(url=reddit_link)
DNE = 'Does Not Exist'


class RedditTitle:
    title = submission.title
    score = submission.score
    num_com = submission.num_comments
    subreddit = submission.subreddit
    try:
        author = submission.author.name
    except:
        author = '[–] ' + '[deleted]'

    def split_self(self, width):
        split = textwrap.wrap(self.title, width=width)
        return split


# class RedditCreation(RedditItem):
#     for i in range(number_comments):  # gets all all comments saves them to a string
#
#         # Creates the comments if they exist
#         try:
#             temp_com = submission.comments[i].replies[0].body.replace('&#x200B', '')
#             temp_com = re.sub(r"\[(.+)\]\(.+\)", r"\1", temp_com)
#         except:
#             temp_com = DNE
#
#         # Creates the authors if they exist
#         if temp_com != DNE:
#             try:
#                 temp_name = ('[–] ' + submission.comments[i].replies[0].author.name)  # and indexes them starting at 0
#             except:
#                 temp_name = ('[–] ' + '[deleted]')
#         else:
#             temp_name = DNE
#
#         try:
#             temp_score = submission.comments[i].replies[0].score
#         except:
#             temp_score = DNE
#         reply_list.append(RedditItem(temp_com, temp_name, temp_score))
#         del temp_com
#         del temp_name
#         del temp_score

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

vid_name = 'Final'
vid_extension = '.mp4'
fullVideoPath = VID_DIR + vid_name + vid_extension

cWidth = 175
rWidth = 168
rtrWidth = 161
VidFPS = 15

# imported with Pillow
BACKGROUND = Image.open('Static/backgroundblack.jpg').convert('RGBA')
COMMENT_VOTE_ICON = Image.open('Static/commentupdown.png').convert('RGBA')
COMMENT_VOTE_ICON = COMMENT_VOTE_ICON.resize((22, 56), Image.ANTIALIAS)
TITLE_VOTE_ICON = Image.open('Static/titleupdown.png').convert('RGBA')
COMMENT_VOTE_ICON = COMMENT_VOTE_ICON  # Revisit Later

# imported with moviepy
TRANSITION = VideoFileClip('Static/NewError.mp4').set_duration(.7).set_fps(VidFPS)
BACKGROUND_MUSIC = AudioFileClip('Static/background.mp3')
OUTRO = VideoFileClip('Static/outro.mp4').set_fps(VidFPS)

BALCON_DIR = os.path.dirname(os.path.abspath("balcon.exe"))
UPLOAD_DIR = os.path.dirname(os.path.abspath('Upload/youtubeuploader_windows_amd64.exe')) + '\\'


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


def minute_format(num, roundto=2):
    minutes = int(abs(num) / 60)
    seconds = round(abs(num) % 60, roundto)
    if num < 0:
        minutes = '-' + str(minutes)
    if roundto == 0:
        seconds = int(seconds)
    if seconds < 10:
        seconds = '0' + str(seconds)
    return str(minutes) + ':' + str(seconds)


def human_format(num):
    if num >= 10000:
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
    line_spacing = 25
    more_spacing = line_spacing
    small_space = 5
    medium_space = 25
    large_space = 35
    indent_spacing = 65

    image_width = 1920
    static_space = 75
    com_img_height = static_space + line_spacing*com_len
    indent = 40
    arrow_indent = indent - 30
    footer_parent = 'permalink  source  embed  save  save-RES  report  give award  reply  hide child comments'
    footer_child = 'permalink  source  embed  save  save-RES  parent  report  give award  reply  hide child comments'
    comment_spacing = 12
    author = comment_list[index].author

    body_font = ImageFont.truetype('CustFont/Verdana.ttf', 20)
    author_font = ImageFont.truetype('CustFont/verdanab.ttf', 15)

    if bool_reply(comment):
        formatted_reply = reply_list[index].split_self(rWidth)
        rep_len = len(formatted_reply)
        rep_height = large_space + line_spacing * rep_len
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

            draw.text((rep_auth_x, rep_auth_y), rep_author, font=author_font, fill="#6bb6ca")
            draw.text((rep_score_x, rep_score_y), f'  {str(rep_score)} points', font=author_font, fill="#B4B4B4")

            img.paste(COMMENT_VOTE_ICON, (indent + arrow_indent, line_height), COMMENT_VOTE_ICON)
            draw.line((indent, img_height - 5, indent, rep_auth_y), fill="#B4B4B4", width=3)

            for rep_string in formatted_reply:
                line_height += line_spacing
                rep_str_num = formatted_reply.index(rep_string)
                draw.text((indent, line_height), rep_string, font=body_font, fill="#dddddd")
                img_path = IMG_DIR + str(index) + '.' + str(1) + '.' + str(rep_str_num) + '.png'
                temp = BACKGROUND.copy()
                temp.paste(img, (0, 540 - int(.5 * img_h)), img)
                temp.save(img_path)

            line_height += medium_space
            draw.text((indent, line_height), footer_child, font=author_font, fill="#828282")
    else:
        rep_height = 0

        def reply():
            pass

    if bool_rtr(comment):
        formatted_rtr = rtr_list[index].split_self(rtrWidth)
        rtr_len = len(formatted_rtr)
        rtr_height = large_space + line_spacing * rtr_len
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

            draw.text((rtr_auth_x, rtr_auth_y), rtr_author, font=author_font,  fill="#6bb6ca")
            draw.text((rtr_score_x, rtr_score_y), f'  {str(rtr_score)}  points', font=author_font, fill="#B4B4B4")
            img.paste(COMMENT_VOTE_ICON, (indent + arrow_indent, line_height), COMMENT_VOTE_ICON)
            draw.line((indent, img_height - 5, indent, rtr_auth_y), fill="#B4B4B4", width=3)

            for rtrString in formatted_rtr:
                line_height += line_spacing
                rtrStringNum = formatted_rtr.index(rtrString)
                draw.text((indent, line_height), rtrString, font=body_font, fill="#dddddd")
                IMGPath = IMG_DIR + str(index) + '.' + str(2) + '.' + str(rtrStringNum) + '.png'
                temp = BACKGROUND.copy()
                temp.paste(img, (0, 540 - int(.5 * img_h)), img)
                temp.save(IMGPath)

            line_height += medium_space
            draw.text((indent, line_height), footer_child, font=author_font, fill="#828282")
    else:
        rtr_height = 0
        def rtr():
                pass



    img_height = static_space + line_spacing*com_len + rep_height + rtr_height

    img = Image.new('RGBA', (image_width, img_height), '#222222')
    draw = ImageDraw.Draw(img)
    img_w, img_h = img.size

    auth_w, auth_h = author_font.getsize(author)
    auth_x, auth_y = (indent, line_height)
    scr_x, scr_y = (auth_w + indent, line_height)
    
    draw.text((auth_x, auth_y), author, font=author_font, fill="#6bb6ca") 
    draw.text((scr_x, scr_y), f'  {str(comment_list[index].score)} points', font=author_font, fill="#B4B4B4")
    img.paste(COMMENT_VOTE_ICON, (arrow_indent, line_height), COMMENT_VOTE_ICON)
    
    for string in formatted_comment:
        line_height += line_spacing
        string_num = formatted_comment.index(string)
        draw.text((indent, line_height), string, font=body_font, fill="#dddddd")
        img_path = IMG_DIR + str(index) + '.' + str(0) + '.' + str(string_num) + '.png'

        temp = BACKGROUND.copy()
        temp.paste(img, (0, 540 - int(.5 * img_h)), img)
        temp.save(img_path)

    line_height += medium_space
    draw.text((indent, line_height), footer_parent, font=author_font, fill="#828282")

    reply()
    rtr()

    photofilepath = IMG_DIR + str(index) + '.png'
    # img.show()


def create_txt(comment):
    index = str_comment_list.index(comment)

    filename = TXT_DIR + str(index) + '.0.txt'
    myFile = open(filename, 'w', encoding='utf-8')  # for some reason as of 6/17/19 1:10 AM IT NEEDS ENCODING
    myFile.write(replace_me(comment, aud_rep, aud_rep_with))
    myFile.close()
    if bool_reply(comment):
        filename = TXT_DIR + str(index) + '.1.txt'
        myFile = open(filename, 'w', encoding='utf-8')  # for some reason as of 6/17/19 1:10 AM IT NEEDS ENCODING
        myFile.write(replace_me(reply_list[index].string, aud_rep, aud_rep_with))
        myFile.close()
    else:
        pass

    if bool_rtr(comment):
        filename = TXT_DIR + str(index) + '.2.txt'
        myFile = open(filename, 'w', encoding='utf-8')  # for some reason as of 6/17/19 1:10 AM IT NEEDS ENCODING
        myFile.write(replace_me(rtr_list[index].string, aud_rep, aud_rep_with))
        myFile.close()
    else:
        pass


def create_wav(comment):
    index = str_comment_list.index(comment)

    def balcon(num):
        os.chdir(BALCON_DIR)  # changes command line directory for the balcon utility
        tFile = str(index) + '.%s.txt' % num
        wFile = str(index) + '.%s.wav' % num
        command = 'balcon -f "Subs\Sub1\Txt\%s"' % tFile + ' -w "Subs\Sub1\Wav\%s"' % wFile + ' -n "ScanSoft Daniel_Full_22kHz"'
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


def createClip(comment):
    index = str_comment_list.index(comment)

    splitCom = comment_list[index].split_self(cWidth)
    splitComLen = len(splitCom)
    splitRep = reply_list[index].split_self(rWidth)
    splitRepLen = len(splitRep)
    splitRTR = rtr_list[index].split_self(rtrWidth)
    splitRTRLen = len(splitRTR)
    cClip = []
    concat = []
    iClip0 = []
    iClip1 = []
    iClip2 = []
    Clip = 0
    a0Path = WAV_DIR + str(index) + '.0.wav'
    a1Path = WAV_DIR + str(index) + '.1.wav'
    a2Path = WAV_DIR + str(index) + '.2.wav'

    sum0 = sum(len(zero) for zero in splitCom)
    sum1 = sum(len(one) for one in splitRep)
    sum2 = sum(len(two) for two in splitRTR)

    aClip0 = AudioFileClip(a0Path)
    for string in splitCom:
        factor = len(string)/sum0
        path = IMG_DIR + str(index) + '.0' + '.%s.png' %splitCom.index(string)
        Clip = ImageClip(path).set_duration(factor * aClip0.duration)
        iClip0.append(Clip)
        #print(path)
    s0 = '\ndone comment: ' + str(index)
    iClip0 = concatenate_videoclips(iClip0)
    iClip0 = iClip0.set_audio(aClip0)
    cClip.append(iClip0)
    if bool_reply(comment):
        aClip1 = AudioFileClip(a1Path)
        for rString in splitRep:
            factor = len(rString)/sum1
            path = IMG_DIR + str(index) + '.1' + '.%s.png' % splitRep.index(rString)
            Clip = ImageClip(path).set_duration(factor * aClip1.duration)
            iClip1.append(Clip)
            #print(path)

        s1 = '\n    done reply: ' + str(index)
        iClip1 = concatenate_videoclips(iClip1)
        iClip1 = iClip1.set_audio(aClip1)
        cClip.append(iClip1)
    else:
        s1 = ''
        pass
    if bool_rtr(comment):
        aClip2 = AudioFileClip(a2Path)
        for rtrString in splitRTR:
            factor = len(rtrString)/sum2
            path = IMG_DIR + str(index) + '.2' + '.%s.png' % splitRTR.index(rtrString)
            Clip = ImageClip(path).set_duration(factor * aClip2.duration)
            iClip2.append(Clip)
            #print(path)
        s2 = '\n        done rtr: ' + str(index)
        iClip2 = concatenate_videoclips(iClip2)
        iClip2 = iClip2.set_audio(aClip2)
        cClip.append(iClip2)
    else:
        s2 = ''
        pass
    cClip.append(TRANSITION)
    cClip = concatenate_videoclips(cClip)
    print(s0, end='')
    print(s1, end='')
    print(s2, end='')
    return cClip


def replace_me(string, to_replace, replace_with):
    if len(to_replace) != len(replace_with):
        CRASH
    for item1, item2 in zip(to_replace, replace_with):
        string = string.replace(item1, item2)
    return string


def create_title_clip():
    titleString = RedditTitle.title
    titlePoints = str(RedditTitle.score)
    titleCommentsNum = str(RedditTitle.num_com)
    try:
        titleAuthor = str(submission.author.name)
    except:
        titleAuthor = '[deleted]'
    submitDate = 'submitted 6 hours ago by'
    tFooter = ' comments  source  share  save  hide  give award  report  crosspost'
    sub = '(self.' + str(submission.subreddit) + ')'
    titleSplit = RedditTitle.split_self(RedditTitle, 70)
    titleStringNum = len(titleSplit)

    pointLenth = len(titlePoints)
    if '.' in titlePoints:
        pointLenth = pointLenth - 1
    else:
        pass
    #print(pointLenth)

    if pointLenth == 3:
        pointIndent = 55
    elif pointLenth == 4:
        pointIndent = 45
    elif pointLenth == 5:
        pointIndent = 35
    elif pointLenth == 6:
        pointIndent = 25
    else:
        pointIndent = 65


    titleIndent = 220

    tHeight = 45 * titleStringNum + 200
    tWidth = 1920
    title = Image.new('RGBA', (tWidth, tHeight), '#222222')
    tdraw = ImageDraw.Draw(title)

    titleFont = ImageFont.truetype('CustFont/Verdana.ttf', 45)
    midFont = ImageFont.truetype('CustFont/Verdana.ttf', 28)
    footerFont = ImageFont.truetype('CustFont/verdanab.ttf', 28)
    pointFont = ImageFont.truetype('CustFont/arial.ttf', 36)
    for i in titleSplit:
        currentHeightTitle = 20 + 45 * titleSplit.index(i)
        tdraw.text((titleIndent, currentHeightTitle), i, font=titleFont, fill="#dedede")
    selfHeight = currentHeightTitle + 60
    tdraw.text((titleIndent, selfHeight), sub, font=midFont, fill="#888888")
    submitHeight = selfHeight + 75
    sw,sh = midFont.getsize(submitDate)
    pw, ph = pointFont.getsize(titlePoints)
    tdraw.text((titleIndent, submitHeight), submitDate, font= midFont, fill="#828282")
    tdraw.text((titleIndent + sw, submitHeight), ' ' + titleAuthor, font=midFont, fill="#6bb6ca")
    tdraw.text((titleIndent, tHeight - 50), titleCommentsNum + tFooter, font=footerFont, fill="#828282")
    tdraw.rectangle([(0,0), (titleIndent-40, tHeight)], fill='#121414', outline='#2E3234', width=4)
    title.paste(TITLE_VOTE_ICON, (55,20), TITLE_VOTE_ICON)

    tdraw.text((pointIndent, 90), titlePoints, font=pointFont, fill='#646464')
    ttemp = BACKGROUND.copy()
    ttemp.paste(title, (0,540 - int(.5* tHeight)), title)

    ttemp.save(IMG_DIR + 'title.png')

    filename = TXT_DIR + 'title.txt'
    myFile = open(filename, 'w', encoding='utf-8')  # for some reason as of 6/17/19 1:10 AM IT NEEDS ENCODING
    myFile.write(replace_me(titleString, aud_rep, aud_rep_with))
    myFile.close()


    os.chdir(BALCON_DIR)  # changes command line directory for the balcon utility
    tFile = 'title.txt'
    wFile = 'title.wav'
    command = 'balcon -f "Subs\Sub1\Txt\%s"' % tFile + ' -w "Subs\Sub1\Wav\%s"' % wFile + ' -n "ScanSoft Daniel_Full_22kHz"'
    os.system(command)
    while not os.path.isfile(WAV_DIR + 'title.wav'):
        time.sleep(.12)

    titleAClip = AudioFileClip(WAV_DIR + 'title.wav')
    titleIClip = ImageClip(IMG_DIR + 'title.png').set_duration(titleAClip.duration)
    titleClip = titleIClip.set_audio(titleAClip)
    titleClip = concatenate_videoclips([titleClip, TRANSITION])
    return titleClip


def cleanup():
    shutil.rmtree(IMG_DIR)
    print('Removed IMG')
    os.mkdir(IMG_DIR)
    print("Created IMG")

    shutil.rmtree(TXT_DIR)
    print('Removed TXT')
    os.mkdir(TXT_DIR)
    print('Created TXT')

    shutil.rmtree(WAV_DIR)
    print('Removed WAV')
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
    if del_vid == True and os.path.isdir(VID_DIR):
        shutil.rmtree(VID_DIR)
        print('Removed VID')
        os.mkdir(VID_DIR)
        print("Created VID")


def create_thumbnail():
    def human_format(num):
        if num >= 1000:
            magnitude = 0
            while abs(num) >= 1000:
                magnitude += 1
                num /= 1000.0
            # add more suffixes if you need them
            return '%.1f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
        else:
            return num

    def color_options():
        backChoice = 2# int(input('\nType your background color option [0 = Transparent, 1 = Default, 2 = Black]\n'))
        if backChoice == 0:
            color = 0
        elif backChoice == 1:
            color = '#222222'
        elif backChoice == 2:
            color = 'black'
        else:
            print('Choice is not recognized reverting to defaults')
            color = '#222222'
        return color

    # date = datetime.datetime.fromtimestamp(submission.created_utc)
    # dif = datetime.datetime.utcnow() - date
    # print(dif)

    thumbSubreddit = 'r/' + str(RedditTitle.subreddit)
    thumbAuthor = 'u/' + str(RedditTitle.author)
    thumbScore = int(RedditTitle.score)
    thumbNumCom = int(RedditTitle.num_com)
    title = RedditTitle.title.replace('/', ' ')
    thumbnail = Image.new('RGBA', (1920, 1080), color_options())  # from #222222
    thumbDraw = ImageDraw.Draw(thumbnail)
    width = 31
    formatedTitle = textwrap.wrap(title, width=width)

    askredditIcon = Image.open('Thumbnail/askreddit.png').resize((100, 100), Image.ANTIALIAS)  # move later
    updownVote = Image.open('Thumbnail/upvotedownvote.png').convert('RGBA')
    updownVote = updownVote.resize((440, 400), Image.ANTIALIAS)
    commentIcon = Image.open('Thumbnail/commenticon.png')
    commentIcon = commentIcon.resize((180, 160), Image.ANTIALIAS)

    iconW, iconH = askredditIcon.size

    size = 90
    subFont = ImageFont.truetype('CustFont/NimbusSanL-Reg.ttf', 75)
    author_font = ImageFont.truetype('CustFont/NimbusSanL-Bol.ttf', 45)
    scoreFont = ImageFont.truetype('CustFont/NimbusSanL-Bol.ttf', 60)

    postedAuthor = 'Posted by ' + thumbAuthor + ' 6 hours ago'
    bodyBaseHeight = 210
    line_spacing = 90
    indentSpacing = 40
    pointX, pointY = -40, 720

    thumbnail.paste(commentIcon, (300, 850), commentIcon)
    thumbnail.paste(updownVote, (pointX, pointY), updownVote)
    thumbDraw.text((iconW + indentSpacing + 30, 120), postedAuthor, font=author_font, fill='#818384')
    thumbnail.paste(askredditIcon, (40, 40), askredditIcon)
    thumbDraw.text((iconW + indentSpacing + 30, 40), thumbSubreddit, font=subFont)
    thumbDraw.text((90, 910), str(human_format(thumbScore)), font=scoreFont, fill='#FF8C60')
    thumbDraw.text((500, 900), str(human_format(thumbNumCom)) + '  Comments', font=scoreFont, fill='#818384')

    lineHeight = bodyBaseHeight
    #print(str(len(formatedTitle) * (size + line_spacing)))
    count_1 = 0
    count_2 = 0
    while (not 1020 <= len(formatedTitle) * (size + line_spacing) <= 1200):
        while (len(formatedTitle) * (size + line_spacing) >= 1200):
            count_1 = count_1 + 1
            size = size - 2
            line_spacing = line_spacing - 2
            width = width + .8
            formatedTitle = textwrap.wrap(title, width=width)
            if (count_1 >= 35):
                break
        while (len(formatedTitle) * (size + line_spacing) <= 1020):
            count_2 = count_2 + 1
            size = size + 2
            line_spacing = line_spacing + 2
            width = width - .8
            formatedTitle = textwrap.wrap(title, width=width)
            if (count_2 >= 35):
                break
        if (count_1 >= 35):
            break
        if (count_2 >= 35):
            break
    # print(str(len(formatedTitle) * (size + line_spacing)))
    # print(count_1, count_2)
    for line in formatedTitle:
        body_font = ImageFont.truetype('CustFont/NimbusSanL-Bol.ttf', size)
        thumbDraw.text((indentSpacing, lineHeight), line, font=body_font)
        lineHeight = lineHeight + line_spacing

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

        if dur_counter > estimatedTime * 1.1:
            break
    song_sound = concatenate_audioclips(song_sound)
    song_sound = song_sound.volumex(.1)
    sound_desc = ''.join(song_info)


df = pd.read_csv('MLData.csv')
reg = linear_model.LinearRegression()
reg.fit(df[['char_len', 'num_com', 'threshold']], df.duration)


def estimate_time():
    global estimatedTime
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

    estimatedTime = reg.predict([[charSum, number_comments, threshold]])[0]
    estimatedTime = round(estimatedTime, 5)
    print('Estimated Video Length is: ' + minute_format(estimatedTime) + ' or ' + str(estimatedTime) + 's')


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
        print("waitng for comment:" + str(index))
    if bool_reply(thing):
        while not os.path.isfile(sp1):
            time.sleep(.3)
            print("waitng for reply:" + str(index))
    else:
        pass
    if bool_rtr(thing):
        while not os.path.isfile(sp2):
            time.sleep(.3)
            print("waitng for comment:" + str(index))
    else:
        pass
    # time.sleep(3)
    final.append(createClip(thing))


def metadata():
    str_tag = 'reddit, best of ask reddit, reddit, ask reddit top posts, r/story, r/ askreddit, r/askreddit, ' \
              'story time, reddify, r slash, toad films, updoot, flumpy, foxfilms, jayben, reddit & chill, bamboozled, ' \
              'brainydude, reddit watchers, best posts & comments, reddit sexual, reddit 2019, reddit nsfw, ' \
              'askreddit nsfw, Reddit Genie'
    data ={
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
                       '\n' + \
                       sound_desc + \
                       '\n'
                       '\nOutro Template made by Grabster - Youtube.com/GrabsterTV'
                       '\n'
                       '\nSubreddits used: r/AskReddit'
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
        # 'recordingdate': '2017-05-21',
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


aud_rep, aud_rep_with = ['’', '‘', '”', '“', '*', ';', '^', 'coworker', 'Coworker', 'tbh', 'omg'], \
                        ["'", "'", '"', '"', '', '', '', 'co-worker', 'co-worker', 'to be honest', 'oh my god']
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
while estimatedTime > tyt:
    number_comments -= 1
    estimate_time()
    if estimatedTime < tyt: break
    for y in range(5):
        threshold += .08
        estimate_time()
        if estimatedTime < tyt: break
    estimate_time()
    if estimatedTime < tyt: break
    threshold = .1
print(number_comments)
print(threshold)

dynamic_music()

final = [create_title_clip()]

thread = []
for com in str_comment_list[:number_comments]:
    ind = str_comment_list.index(com)
    temp = threading.Thread(target=video_creation, args=(com,))
    thread.append(temp)
    thread[ind].start()
for com in str_comment_list[:number_comments]:
    index = str_comment_list.index(com)
    thread[index].join()

final.append(OUTRO)
final = concatenate_videoclips(final)
backgroundMusic = song_sound.set_duration(final.duration)
final_audio = CompositeAudioClip([final.audio, backgroundMusic])
final = final.set_audio(final_audio)
strong = round(100 - (abs(estimatedTime/final.duration) * 100), 2)
if strong > 0:
    strong = '+' + str(strong)
else:
    strong = str(strong)
weakSauce = final.duration - estimatedTime
weak = minute_format(weakSauce)
if float(weakSauce) > 0:
    weak = '+' + weak
else:
    pass

print('\n \nActual Video Lenth is: ' + minute_format(final.duration) + ' / ' + str(final.duration) + 's. Shifted ' +
      weak + ' / ' + str(strong) + '%' + ' from ' + minute_format(estimatedTime) + ' / ' + str(final.duration) + 's')
print('\n')
metadata()
# final.write_videofile(fullVideoPath, fps=VidFPS, threads=16, preset='ultrafast')
#
# shutil.copy2(fullVideoPath, UPLOAD_DIR)
# shutil.copy2(VID_DIR + 'thumb.png', UPLOAD_DIR)
#
# # upload_video()
# data_collection()
# cleanup()

