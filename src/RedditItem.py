import directories

from praw.models import Submission
import datetime
import textwrap
from PIL import Image, ImageFont, ImageDraw


directories.init()
class RedditItem:
    # Imported with Pillow - Gildings
    gild_w, gild_h = (20, 20)
    PLATINUM = Image.open(f'{directories.ICON_DIR}platinum.png')
    PLATINUM = PLATINUM.resize((gild_w, gild_h), Image.ANTIALIAS)
    GOLD = Image.open(f'{directories.ICON_DIR}gold.png')
    GOLD = GOLD.resize((gild_w, gild_h), Image.ANTIALIAS)
    SILVER = Image.open(f'{directories.ICON_DIR}silver.png')
    SILVER = SILVER.resize((gild_w, gild_h), Image.ANTIALIAS)
    icon_img_font = ImageFont.truetype('CustFont/verdanab.ttf', 17)

    def __init__(self, *args):

        # def __init__(self, sub : Submission):
        if isinstance(args[0], Submission):
            self.title = args[0].title
            self.body = args[0].selftext
            self.author = args[0].author
            self.subreddit = args[0].subreddit
            self.score = args[0].score
            self.created = datetime.datetime.fromtimestamp(args[0].created)
            self.num_com = args[0].num_comments
            try:
                self.author = args[0].author.name
            except AttributeError:
                self.author = '[deleted]'

        # def __init__(self, body : str, author : str, score : int, time_ago : int, gildings : list, include=True):
        elif isinstance(args[0], str) and isinstance(args[1], str) and (isinstance(args[2], int) or isinstance(args[3], str)) \
            and isinstance(args[3], str): # and isinstance(args[4], list):
            self.body = args[0]
            self.author = args[1]
            self.score = args[2]
            self.time_ago = args[3]
            self.gildings = args[4]
            self.include = True

            if len(args) > 5:
                if args[5] == False:
                    self.include = False

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

            # Draws the awards given to a specific comment
            # if a given comment has more than one type of award, then we draw a count next to the award
            if num_silver >= 1:
                icon_img.paste(self.SILVER, (current_width, 0), self.SILVER)
                current_width += self.gild_w
                more_space = spacing
            if num_silver >= 2:
                current_width += small_spacing
                icon_img_draw.text((current_width, text_height), str(num_silver), font=self.icon_img_font,
                                   fill='#6a98af')
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
                icon_img_draw.text((current_width, text_height), str(num_platinum), font=self.icon_img_font,
                                   fill='#6a98af')
                current_width += spacing

            self.icon = icon_img
        else:
            print("Error initiailizing RedditItem")
            for arg in args:
                print(arg)
            print(isinstance(args[1], str))
            sys.exit()

    def split_self(self, width):
        """
        Function:   split_self
        Definition: Takes the string of the comment and splits the string into lines of length: width
        Parameter:  width
        Return:     List
        """
        split = textwrap.wrap(self.body, width=width)
        return split

    def get_split_len(self, width):
        """
        Function:   get_split_len
        Definition: returns the length of a string that was split with width: width
        Parameter:  width
        Return:     Integer
        """
        split_len = textwrap.wrap(self.body, width=width)
        return len(split_len)