import time

## import all side functions
from helper import *
from perm import *

def generate_word_list(ws_pair_list, new_hand):
    """
    Objective (A): from new_hand, get all the possible permutations of
    valid words, excluding single words (as they are not included inside
    word_list).
    Objective (B): for each permutation obtained, further obtain the word-
    score pair as a dictionary.
    Objective (C): As there can be duplicate letters, there will be a resultant
    duplicate permutation, so some care has to be given in preventing the
    adding of duplicates.
    Objective (D): if no possible further permutation for a given hand, then
    put back the existing ws_pair, else combine the existing ws_pair with new
    ws_pair.
    Objective (E): if new_hand is empty i.e. letters are all used up, then just
    put in the existing ws_pair, and move on with next hand option. 

    ws_pair_list: list (dictionary)
    new_hand: list (dictionary)
    returns: list (dictionary)
    """
    new_ws_pair_list = []
    for i in range(len(new_hand)):
        hand_length = int()
        sub_pair_list = []
        if len(new_hand[i]) == 0: # (E)
            new_ws_pair_list.append(ws_pair_list[i])
        else:
            for each in new_hand[i]:
                hand_length += new_hand[i][each]
            for x in range(hand_length-1):
                perm_list = get_perms(new_hand[i], hand_length-x) # (A)
                for word in perm_list:
                    if word in word_list:
                        pair = update_pair(word) # (B)
                        if pair not in sub_pair_list: # (C)
                            sub_pair_list.append(pair) 
            if len(sub_pair_list) == 0: # (D)
                new_ws_pair_list.append(ws_pair_list[i])
            else:
                for each_sub in sub_pair_list:
                    new_ws_pair_list.append(merge_two_dicts(ws_pair_list[i], each_sub))
    return new_ws_pair_list

def cycle_recursive(ws_pair_list, initial_hand, new_hand):
    """
    A recursive function that repeats the generating increasing possibilities
    of ws_pairs. Only condition to break out of it is to obtain a pair_list that
    does not differ from the previous. Then again would a while loop be more
    efficient in terms of performance and memory? Especially since this is a
    tail recursion?
    
    ws_pair_list: list (dictionary)
    initial_hand: dictionary
    new_hand: list (dictionary)
    returns: list (dictionary)
    """
    start = time.time()

    answer = generate_word_list(ws_pair_list, new_hand)
    new_hand = hand_from_word(answer, initial_hand)
    
    end = time.time()
    print ('Time taken for this cycle: ', end-start, 'seconds')

    if ws_pair_list != answer:
        return cycle_recursive(answer, initial_hand, new_hand)
    else:
        return answer

def cycle_iterative(ws_pair_list, initial_hand, new_hand):
    """
    An identical iterative version of the cycle. For some reason the
    processing speed is the same. Means to say, since python does not
    exercise a TRO, this is the more apt choice/solution. 

    ws_pair_list: list (dictionary)
    initial_hand: dictionary
    new_hand: list (dictionary)
    returns: list (dictionary)
    """
    memory_pair = []
    while True:
        start = time.time()
        memory_pair = ws_pair_list
        ws_pair_list = generate_word_list(ws_pair_list, new_hand)
        new_hand = hand_from_word(ws_pair_list, initial_hand)
        
        end = time.time()
        print ('Time taken for this cycle: ', end-start, 'seconds')
        if memory_pair == ws_pair_list:
            return ws_pair_list

if __name__ == '__main__':
    
    ## Loading resources
    word_list = load_words()
    initial_hand = deal_hand(HAND_SIZE)
    print ('HAND: ', initial_hand)

    ## Begins the recursive cycle function call, taking initial_hand
    ## as the starting arguments. new_hand requires a list of hand
    ## dictionaries
    final_list = cycle_iterative([{}], initial_hand, [initial_hand])
##    final_list = cycle_recursive([{}], initial_hand, [initial_hand])

    ## Conducts final refinements to obtain optimal answer
    refined_list = refine_list(final_list)
    score_list = return_total_score(refined_list)
    max_ws_list, max_value = get_max_ws(refined_list, score_list)

    ## prints user the necessary information
    print ('Best solution(s): ', max_ws_list)
    print ('Total Score: ', max_value)
    
            
    
