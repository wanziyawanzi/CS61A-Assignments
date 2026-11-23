"""Typing test implementation"""

from utils import (
    lower,
    split,
    remove_punctuation,
    lines_from_file,
    count,
    deep_convert_to_tuple,
)
from ucb import main, interact, trace
from datetime import datetime
import random


###########
# Phase 1 #
###########


def pick(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which the SELECT returns True.
    If there are fewer than K such paragraphs, return an empty string.
    返回第 k 个满足 select 函数的段落。如果不存在这样的段落
    （因为 k 大于或等于符合条件的段落数量），那么 pick 返回空字符串
    
    Arguments:
        paragraphs: a list of strings representing paragraphs 段落的列表
        select: a function that returns True for paragraphs that meet its criteria
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    l_ps = [item for item in paragraphs if select(item)]
    return l_ps[k] if k < len(l_ps) else ''
    # END PROBLEM 1


def about(subject):
    """Return a function that takes in a paragraph and returns whether
    that paragraph contains one of the words in SUBJECT.
    返回一个函数，该函数接受一个段落，并返回该段落是否包含 SUBJECT 中的任意一个单词
    
    Arguments:
        subject: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in subject]), "subjects should be lowercase."

    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def f(ps):
        new_ps=split(lower(remove_punctuation(ps)))
        for item in subject:
            for i in new_ps:
                if i == item:
                    return True
        return False
    return f
    # END PROBLEM 2


def accuracy(typed, source):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    compared to the corresponding words in SOURCE.
    它返回 typed 中与 source 中对应单词完全匹配的单词百分比。大小写和标点也必须匹配。
    “对应”在这里意味着两个单词必须出现在 typed 和 source 中的相同索引处.
    
    这个函数衡量的是：你已经输入的单词里，有多少个和 source 对应位置的单词完全一样

    Arguments:
        typed: a string that may contain typos
        source: a model string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)  #单词列表
    source_words = split(source)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if not typed_words:
        return 100.0 if not source_words else 0.0
    n = sum(t ==s for t,s in zip(typed_words,source_words))
    '''if len(typed_words) <= len(source_words):
        for i in range(len(typed_words)):
            if typed_words[i] == source_words[i]:
                n += 1
    else:
        for i in range(len(source_words)):
            if typed_words[i] == source_words[i]:
                n += 1'''
    return n*100/len(typed_words)
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, "Elapsed time must be positive"
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return len(typed)/5/(elapsed/60)
    # END PROBLEM 4


################
# Phase 4 (EC) #
################


def memo(f):
    """A general memoization decorator."""
    cache = {}

    def memoized(*args):
        immutable_args = deep_convert_to_tuple(args)  # convert *args into a tuple representation
        if immutable_args not in cache:
            result = f(*immutable_args)
            cache[immutable_args] = result
            return result
        return cache[immutable_args]

    return memoized


def memo_diff(diff_function):
    """A memoization function."""
    cache = {}

    def memoized(typed, source, limit):
        # BEGIN PROBLEM EC
        "*** YOUR CODE HERE ***"
        # END PROBLEM EC

    return memoized


###########
# Phase 2 #
###########


def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD based on DIFF_FUNCTION. If multiple words are tied for the smallest difference,
    return the one that appears closest to the front of WORD_LIST. If the
    difference is greater than LIMIT, return TYPED_WORD instead.
    如果 typed_word 包含在 word_list 中,autocorrect 返回该单词。
    否则 autocorrect 返回 word_list 中与提供的 typed_word 差异最低的单词。这个差异是 
    diff_function 返回的数字。
    但是，如果 typed_word 与 word_list 中任何单词之间的最低差异大于 limit,则返回 typed_word。
    换句话说,limit 设置了一个最大阈值，表示一个拼写错误严重到什么程度仍然可以被纠正。
    
    Arguments:
        typed_word: a string representing a word that may contain typos
        word_list: a list of strings representing source words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    if typed_word in word_list:
        return typed_word
    else:
        diff = [diff_function(typed_word,item,limit) for item in word_list]
        min_diff = min(diff,key=abs)
        if abs(min_diff) > limit:
            return typed_word
        else:
            return word_list[diff.index(min_diff)]
    # END PROBLEM 5


def furry_fixes(typed, source, limit):
    """A diff function for autocorrect that determines how many letters
    in TYPED need to be substituted to create SOURCE, then adds the difference in
    their lengths and returns the result.
    这个函数接受两个字符串，并返回将输入单词转换为源单词所需更改的最小字符数。
    如果两个字符串长度不相等，长度差会加入总差异计数。
    
    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> furry_fixes("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> furry_fixes("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> furry_fixes("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> furry_fixes("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> furry_fixes("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    def f(w1,w2,limit,diff):
        if diff > limit:
            return diff
        if w1[0] != w2[0]: #判断字符
            diff += 1
        if len(w1) == 1: #判断长度 两个维度
            return diff 
        else:
            return f(w1[1:],w2[1:],limit,diff)
              
    length = abs(len(typed) - len(source))
    if length > limit:
        return length 
    if len(typed) >= len(source):
        return length + f(typed[:len(source)],source,limit-length,0)
    else:
        return length + f(typed,source[:len(typed)],limit-length,0)
    # END PROBLEM 6


def minimum_mewtations(typed, source, limit):
    """A diff function for autocorrect that computes the edit distance from TYPED to SOURCE.
    This function takes in a string TYPED, a string SOURCE, and a number LIMIT.
    更高级的 diff 函数，它返回将输入单词转换为源单词所需的最少编辑操作数
    
    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of edits

    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """
    '''def f(w1,w2,limit,diff):  自己尝试且测试通过的复杂思路,人为判断哪种操作最优
        if diff > limit: # Base cases should go here, you may add more base cases as needed.
            # BEGIN
            "*** YOUR CODE HERE ***"
            return diff
            # END
        # Recursive cases should go below here
        if len(w2) == 1:
            if len(w1) == 1:
                return diff if w1 == w2 else diff+1
            else:
                return diff+len(w1)-1 if w2 in w1 else diff+len(w1)
        elif len(w1) == 1:
            return diff+len(w2)-1 if w1 in w2 else diff+len(w2)       
        elif w1[0] == w2[0]: # Feel free to remove or add additional cases 可以随意删除或添加额外的用例
            # BEGIN
            "*** YOUR CODE HERE ***"
            return f(w1[1:],w2[1:],limit,diff)
            # END
        else:
            add = w2[0]+w1 # Fill in these lines
            remove = w1[1:]
            substitute = w2[0]+w1[1:]
            diff += 1
            # BEGIN
            "*** YOUR CODE HERE ***"
            if w1[1] == w2[1]:  #二位相等
                if len(w1) == 2:
                    if w1[0] == w2[1]:
                        return f(add,w2,limit,diff)
                    else: return f(substitute,w2,limit,diff)
                if len(w2) == 2:
                    if w1[1] == w2[0]:
                        return f(remove,w2,limit,diff)
                    else: return f(substitute,w2,limit,diff)
                return f(substitute,w2,limit,diff)
            elif w1[0] == w2[1]:    #一位检测
                return f(add,w2,limit,diff)
            elif w1[1] == w2[0]:
                return f(remove,w2,limit,diff)
            elif len(w2) > 2:
                if w1[0] == w2[2]:    #二位检测
                    return f(add,w2,limit,diff)
                elif len(w1) > 2:
                    if w2[0] == w1[2]:
                        return f(remove,w2,limit,diff)
                    else:
                        return f(substitute,w2,limit,diff)
                else:
                    return f(substitute,w2,limit,diff)
            elif len(w2) == 2:
                if len(w1) > 2:
                    if w2[0] == w1[2]:
                        return f(remove,w2,limit,diff)
                    else:
                        return f(substitute,w2,limit,diff)
                else:
                    return f(substitute,w2,limit,diff)
            else:
                return f(substitute,w2,limit,diff)
            # END
    if typed and source:
        return f(typed,source,limit,0)
    elif (typed or source) == '':
        return abs(len(typed)-len(source))
    else:
        return 0
    局部最优不等于全局最优，不同选择之间存在复杂相互作用，没有可证明的贪心规则'''
    def h(w1,w2,limit,diff):
        if diff > limit:
            return diff 
        if not w1 or not w2:
            return diff+len(w1)+len(w2)
        if w1[0] == w2[0]:
            return h(w1[1:],w2[1:],limit,diff)
        else:
            add = w2[0]+w1 # Fill in these lines
            remove = w1[1:]
            substitute = w2[0]+w1[1:]            
            return min(h(add,w2,limit,diff+1),h(remove,w2,limit,diff+1),h(substitute,w2,limit,diff+1))
    return h(typed,source,limit,0)
# Ignore the line below
minimum_mewtations = count(minimum_mewtations)


def final_diff(typed, source, limit):
    """A diff function that takes in a string TYPED, a string SOURCE, and a number LIMIT.
    If you implement this function, it will be used."""
    def h(w1,w2,limit,diff):
        if diff > limit:
            return diff 
        if not w1 or not w2:
            return diff+len(w1)+len(w2)
        if w1[0] == w2[0]:
            return h(w1[1:],w2[1:],limit,diff)
        else:
            add = w2[0]+w1 # Fill in these lines
            remove = w1[1:]
            substitute = w2[0]+w1[1:]
            if min(len(w1),len(w2)) >1 and w1[1] ==w2[0] and w1[0] == w2[1]:
                substitute = w2[:2]+w1[2:]             
            return min(h(add,w2,limit,diff+1),h(remove,w2,limit,diff+1),h(substitute,w2,limit,diff+1))
    return h(typed,source,limit,0)


FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(typed, source, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.
    你的 report_progress 函数应该做两件事：向多人服务器上传一条消息，并返回该 user_id 玩家的进度。

    要向多人服务器上传消息，请调用 upload 函数，传入一个包含键 'id' 和 'progress' 的两项字典。
    然后该函数应返回玩家的进度，也就是你计算出的单词比例。
    Arguments:
        typed: a list of the words typed so far
        source: a list of the words in the typing source
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> typed = ['how', 'are', 'you']
    >>> source = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(typed, source, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], source, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    cnt = 0
    for i in range(len(typed)):
        if typed[i] == source[i]:
            cnt += 1
        else: break
    progress = cnt/len(source)
    upload({'id':user_id,'progress':progress})
    return progress
    # END PROBLEM 8


def time_per_word(words, timestamps_per_player):
    """Return a dictionary {'words': words, 'times': times} where times
    is a list of lists that stores the durations it took each player to type
    each word in words.
    该函数应返回一个字典，包含两个值：
    -玩家们正在输入的单词列表。
    -一个列表的列表 times,存储每个玩家输入每个单词所花费的时间。
    具体来说,times[i][j] 应表示玩家 i 输入 words[j] 所花费的时间。
    
    Arguments:
        words: a list of words, in the order they are typed.玩家们正在输入的单词列表
        timestamps_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time the
                          player finished typing each word.
                        一个列表的列表，其中每个内部列表包含每个玩家完成输入 
                        words 中每个单词时的时间戳
    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> result = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> result['words']
    ['collar', 'plush', 'blush', 'repute']
    >>> result['times']
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    tpp = timestamps_per_player  # A shorter name (for convenience)
    # BEGIN PROBLEM 9
    times = []  # You may remove this line
    for item in tpp:
        time = [item[i+1]-item[i] for i in range(len(item)-1)]
        times.append(time)
    # END PROBLEM 9
    return {'words': words, 'times': times}


def fastest_words(words_and_times):
    """Return a list of lists indicating which words each player typed fastests.
    返回一个单词列表的列表，每个玩家一个列表。每个玩家的列表包含他们比所有其他玩家输入更快的单词。
    如果出现平局，索引最小的玩家被认为输入该单词最快。
    
    返回每个玩家输入最快的单词。这个函数会在所有玩家完成打字后调用。它接受 time_per_word 返回的字典
    Arguments:
        words_and_times: a dictionary {'words': words, 'times': times} where
        words is a list of the words typed and times is a list of lists of times
        spent by each player typing each word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words({'words': ['Just', 'have', 'fun'], 'times': [p0, p1]})
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    check_words_and_times(words_and_times)  # verify that the input is properly formed
    words, times = words_and_times['words'], words_and_times['times']
    player_indices = range(len(times))  # contains an *index* for each player
    word_indices = range(len(words))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    fast_words = [[] for _ in player_indices]
    for word_index in word_indices:
        time = [get_time(times,player_num,word_index) for player_num in player_indices]
        i = time.index(min(time))
        fast_words[i].append(words[word_index])
    return fast_words
    # END PROBLEM 10


def check_words_and_times(words_and_times):
    """Check that words_and_times is a {'words': words, 'times': times} dictionary
    in which each element of times is a list of numbers the same length as words.
    """
    assert 'words' in words_and_times and 'times' in words_and_times and len(words_and_times) == 2
    words, times = words_and_times['words'], words_and_times['times']
    assert all([type(w) == str for w in words]), "words should be a list of strings"
    assert all([type(t) == list for t in times]), "times should be a list of lists"
    assert all([isinstance(i, (int, float)) for t in times for i in t]), "times lists should contain numbers"
    assert all([len(t) == len(words) for t in times]), "There should be one word per time."


def get_time(times, player_num, word_index):
    """Return the time it took player_num to type the word at word_index,
    given a list of lists of times returned by time_per_word.
    给定由 `time_per_word` 返回的一个“列表的列表”形式的时间数据，
    返回 `player_num` 输入 `word_index` 位置的单词所花费的时间。"""
    num_players = len(times)
    num_words = len(times[0])
    assert word_index < len(times[0]), f"word_index {word_index} outside of 0 to {num_words-1}"
    assert player_num < len(times), f"player_num {player_num} outside of 0 to {num_players-1}"
    return times[player_num][word_index]


enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file("data/sample_paragraphs.txt")
    random.shuffle(paragraphs)
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print("No more paragraphs about", topics, "are available.")
            return
        print("Type the following paragraph and then press enter/return.")
        print("If you only type part of it, you will be scored only on that part.\n")
        print(source)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print("Goodbye.")
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print("Words per minute:", wpm(typed, elapsed))
        print("Accuracy:        ", accuracy(typed, source))

        print("\nPress enter/return for the next paragraph or type q to quit.")
        if input().strip() == "q":
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse

    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument("topic", help="Topic word", nargs="*")
    parser.add_argument("-t", help="Run typing test", action="store_true")

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)