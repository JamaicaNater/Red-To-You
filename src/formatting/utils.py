import itertools

def permutate_word(s):
    """
    Function:   permutate_word
    Definition: this function accepts a word and returns a list of all possible capitalizations for a given word
    Parameter:  a string
    Return:     a list of strings
    """
    return list(''.join(t) for t in itertools.product(*zip(s.lower(), s.upper())))


def replace_me(string, to_replace, replace_with, use_for_audio=False):
    """
    Function:   replace_me
    Definition: The function, given a string, will find and replace the words in the passed argument list
    Parameter:  String, List(Strings), List(Strings), Boolean
    Return:     String
    """
    if len(to_replace) != len(replace_with):
        print("Error in replace_me: Replacement list Desyncronized")
        sys.exit()
    for item1, item2 in zip(to_replace, replace_with):
        string = string.replace(item1, item2)
    if use_for_audio:
        # if reddit_post.subreddit == 'relationships' or 'relationship_advice':
        #     # string = re.sub(r'[\(\[]?[0-9]+[FfMm][\)\]]? ', r'\0', string)
        pass

    return string


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