from PIL import Image
import directories

def init(mode, num_com):
    # Imported with Pillow
    global BACKGROUND
    global COMMENT_VOTE_ICON
    global TITLE_VOTE_ICON #unused
    global SUB_SCORE_ICON
    # Imported with Pillow - Thumbnail Items
    global ASKREDDIT_ICON
    global UPDOWNVOTE
    global COMMENT_ICON

    # Lists font Directories
    global TITLE_FONT_DIR
    global BODY_FONT_DIR
    global SUB_FONT_DIR
    global AUTHOR_FONT_DIR
    global TIME_FONT_DIR
    global FOOTER_FONT_DIR
    global SCORE_FONT_DIR

    # Lists all the hex code for fill
    global AUTHOR_HEX
    global SCORE_HEX
    global TIME_HEX
    global BODY_HEX
    global FOOTER_HEX
    global TITLE_HEX
    global BIG_SCORE_HEX #unused
    global IMG_COLOR
    global TITLE_FOOTER
    global PARENT_FOOTER
    global CHILD_FOOTER

    BACKGROUND = Image.open(f'{directories.ICON_DIR}backgroundblack.jpg') \
                        .convert('RGBA')
    if mode == 0:
        COMMENT_VOTE_ICON = Image.open(f'{directories.ICON_DIR}commentupdown_2.png') \
                                 .convert('RGBA') \
                                 .resize((22, 56), Image.ANTIALIAS)
    else:
        COMMENT_VOTE_ICON = Image.open(f'{directories.ICON_DIR}commentupdown.png') \
                                 .convert('RGBA') \
                                 .resize((22, 56), Image.ANTIALIAS)

    TITLE_VOTE_ICON = Image.open(f'{directories.ICON_DIR}titleupdown.png').convert('RGBA')
    COMMENT_VOTE_ICON = COMMENT_VOTE_ICON  # Revisit Later
    SUB_SCORE_ICON = Image.open(f'{directories.ICON_DIR}sub_up_down.png') \
                          .convert('RGBA') \
                          .resize((28, 73), Image.ANTIALIAS)
    # Imported with Pillow - Thumbnail Items
    ASKREDDIT_ICON = Image.open('Thumbnail/askreddit.png') \
                          .resize((100, 100), Image.ANTIALIAS)  # move later
    UPDOWNVOTE = Image.open('Thumbnail/upvotedownvote.png') \
                      .convert('RGBA') \
                      .resize((440, 400), Image.ANTIALIAS)
    COMMENT_ICON = Image.open('Thumbnail/commenticon.png') \
                        .resize((180, 160), Image.ANTIALIAS)

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
        IMG_COLOR = '#1a1a1b'

        TITLE_FOOTER = str(num_com) + ' Comments   Give Award   Share'
        PARENT_FOOTER = 'Reply   Give Award  Share   Report   Save'
        CHILD_FOOTER = PARENT_FOOTER

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

        TITLE_FOOTER = str(num_com) + ' comments  source  share  save  hide  give award  report  crosspost  ' \
                                                ' hide all child comments'
        PARENT_FOOTER = 'permalink  source  embed  save  save-RES  report  give award  reply  hide child comments'
        CHILD_FOOTER = 'permalink  source  embed  save  save-RES  parent  report  give award  reply  hide child comments'