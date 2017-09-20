import string
import random
import math

"""
Set of constants used throughout helper functions
"""

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words.txt"

"""
Content List of functions:
1a. load_words()
1b. deal_hand()

2a. get_frequency_dict()
2b. get_word_score()
2c. update_pair()

3a. update_hand()
3b. hand_from_word()

4a. merge_two_dicts()

5a. refine_list()
5b. get_letters_used()
5c. return_total_score()
5d. get_max_ws()

"""

"""
(1)
"""

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.

    returns: list
    """
    print ("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print ("  ", len(wordlist), "words loaded.")
    return wordlist

def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = math.ceil(n/3)
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

"""
(2)
"""

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary (string -> int)
    """
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

def get_word_score(word):
    """
    Returns the score of the single word. Not inclusive of the condition
    where all letters are used up.

    word: string (lowercase letters)
    returns: int >= 0
    """
    score = int()
    freq = get_frequency_dict(word)
    for each in freq:
        score += SCRABBLE_LETTER_VALUES[each]*freq[each]
    score = score*len(word)
    return score

def update_pair(word):
    """
    Returns a dictionary containing the word-score pair. This facilitates
    the branching of possibilities and merging of existing and new pair

    word: string (lowercase letters)
    returns: dict (string -> int)
    """
    return {word: get_word_score(word)}

"""
(3)
"""

def update_hand(hand, word):
    """
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    # TO DO ...
    new_hand = hand.copy()
    for each in word:
        new_hand[each] -= 1
    return new_hand

def hand_from_word(ws_pair_list, hand):
    """
    Takes as arguments the current list of words (scores not
    required), as well as the initial hand. Returns a list of
    hand dictionaries for each case.

    ws_pair_list: list (dictionary)
    hand: dictionary (string -> int)
    returns: list (dictionary)
    """
    new_hand = []
    for each_path in ws_pair_list:
        temp_hand = hand
        key_list = each_path.keys()
        for each_key in key_list:
            temp_hand = update_hand(temp_hand, each_key)
        for each in list(temp_hand):
            if temp_hand[each] == 0:
                temp_hand.pop(each)
        new_hand.append(temp_hand)
    return new_hand

"""
(4)
"""

def merge_two_dicts(x, y):
    """
    Given two dicts, merge them into a new dict as a shallow copy.
    This avoids the problem (dictionary) being mutable

    x: dictionary (string -> int)
    y: dictionary (string -> int)
    returns: dictionary (string -> int)
    """
    z = x.copy()
    z.update(y)
    return z

"""
(5)
"""

def refine_list(final_list):
    """
    Given that there will be duplicates in the final_list, arising
    from the order in which words are formed, it is our goal to
    remove those duplicates.

    final_list: list (dictionary)
    refined_list: list (dictionary)
    """
    refined_list = []
    for item in final_list:
        if item not in refined_list:
            refined_list.append(item)
    return refined_list

def get_letters_used(path_list):
    """
    Gets total letters used throughout the multiple words formed
    from each path. For use in calculating bonus points at the end.
    Bonus points are designed to be calculated at the end so as to
    facilitate the dropping of duplicates. If bonus points were added
    to the last word formed i.e. {'yeuky': 75, 'ad': 56} and {'ad': 6,
    'yeuky': 125}, then these two dictionaries are not equal and cannot
    be dropped off.

    path_list: dictionary (string -> int)
    returns: int
    """
    letters_used = int()
    for each_word in path_list.keys():
        for each_letter in each_word:
            letters_used += 1
    return letters_used

def return_total_score(refined_list):
    """
    Takes into account every points scored per word, plus the possible
    bonus points. Returns a list of identical length and corresponding
    index to refined_list so as to generate any ws_list and total_score
    pair.

    refined_list: list (dictionary)
    returns: list (ints)
    """
    score_list = []
    for each_path in refined_list:
        score = int()
        if HAND_SIZE == get_letters_used(each_path):
            score += 50
        for each in each_path.values():
            score += each
        score_list.append(score)
    return score_list

def get_max_ws(refined_list, score_list):
    """
    Returns a list of all possible plays and the corresponding score by
    matching their indexes.

    refined_list: list (dictionary)
    score_list: list (ints)
    returns: list (dictionary), int
    """
    max_ws_list = []
    max_value = max(score_list)
    for i in range(len(score_list)):
        if score_list[i] == max_value:
            max_ws_list.append(refined_list[i])
    return max_ws_list, max_value
