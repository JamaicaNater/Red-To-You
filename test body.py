from PIL import Image, ImageFont, ImageDraw
import praw
import textwrap
import datetime

reddit = praw.Reddit(client_id='BHUtkEY0x4vomA', client_secret='MZvTVUs83p8wEN_Z8EU8bIUjGTY',
                     user_agent='pulling posts')
link = 'https://www.reddit.com/r/confessions/comments/bcxd98/i_kicked_all_my_friends_off_my_hbo_account/'
submission = reddit.submission(url=link)

title = submission.title
body = submission.selftext
author = submission.author
subreddit = submission.subreddit
points = submission.score
created = datetime.datetime.fromtimestamp(submission.created)
num_comments = submission.num_comments
sub_time = datetime.datetime.now() - created + datetime.timedelta(hours=8)

SUB_SCORE_ICON = Image.open('Static/sub_up_down.png').convert('RGBA')
SUB_SCORE_ICON = SUB_SCORE_ICON.resize((28, 73), Image.ANTIALIAS)
BACKGROUND = Image.open('Static/backgroundblack.jpg').convert('RGBA')


def human_format(num):
    if num > 100000:
        num = int(num/1000)*1000
        print('doing something')
        print(num)
    if num >= 10000:
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        # add more suffixes if you need them
        return '%.1f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
    else:
        return num


def human_time(time):
    seconds = time.total_seconds()
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


def create_sub():
    size = 20
    width = 180

    author_font = ImageFont.truetype('CustFont/Verdana.ttf', 15)
    score_font = ImageFont.truetype('CustFont/verdanab.ttf', size - 3)
    title_font = ImageFont.truetype('CustFont/Verdana.ttf', size)
    body_font = ImageFont.truetype('CustFont/Verdana.ttf', size - 2)
    sub_font = ImageFont.truetype('CustFont/Verdana.ttf', size - 6)
    footer_font = ImageFont.truetype('CustFont/verdanab.ttf', size - 6)

    formatted_title = textwrap.wrap(title, width=width)
    formatted_body = textwrap.wrap(body, width=width + 8)
    post_date_by = 'submitted ' + human_time(sub_time) + ' by '
    footer = str(num_comments) + ' comments  source  share  save  hide  give award  report  crosspost  ' \
                                 'hide all child comments'
    formatted_points = str(human_format(points)).replace('.0', '')

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
    sub_draw.text((indent, line_height + 26), formatted_points, font=score_font, fill='#646464')

    # Writes each line in the title
    for line in formatted_title:
        sub_draw.text((indent_spacing, line_height), line, font=title_font, fill='#dedede')
        if line == formatted_title[-1]:
            the_sizex, the_sizey = title_font.getsize(formatted_title[-1])
            sub_draw.text((indent_spacing + the_sizex + 5, line_height + 5), '(self.' + str(subreddit) + ')',
                          font=sub_font, fill='#888888')
        line_height = line_height + line_spacing
    del line

    # Adds spacing then writes the post date and author
    line_height += small_space
    sub_draw.text((indent_spacing, line_height), post_date_by, font=author_font, fill='#828282')
    rrx, rry = author_font.getsize(post_date_by)
    sub_draw.text((indent_spacing + rrx, line_height), ' ' + str(author), font=author_font, fill='#6a98af')
    line_height += small_space

    if body != '':
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
    sub_draw.text((indent_spacing, line_height), footer, font=footer_font, fill='#828282')

    sub_img.show()


create_sub()
