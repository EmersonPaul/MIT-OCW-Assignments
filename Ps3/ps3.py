# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string
import copy

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    '*':0,'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    
    word = word.lower()
    word_length = len(word)
    first_component = 0 # Initial points per letter

    # Iterates over the the string variable: word, and checks corresponding point of each letter
    # by looping through the SCRABBLE_LETTER_VALUES dictionary using 'nested loop 0'
    for a_key in word:
        for a_letter in SCRABBLE_LETTER_VALUES: # This is 'nested loop 0'
            if a_key == a_letter:
                first_component += SCRABBLE_LETTER_VALUES[a_key]
                break # Breaks 'nested loop 0' once same letter is found and points are added

    # Computation for the second component of the score
    second_component = 7 * word_length - 3 * (n - word_length)
    
    if second_component < 1:
        second_component = 1

    return first_component * second_component

    
#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3)) - 1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels + 1, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    x = '*'
    hand[x] = 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    updated_hand = {}
    # Turn letters in the string: word to lowercase 
    # before converting to dictionary with letter frequency(int) as value
    word_dictionary = get_frequency_dict(word.lower()) 

    # Loops through hand to check if each keys are also in word_dictionary
    for a_letter in hand:
        if a_letter in word_dictionary:
            # Gets frequency of letters by subtracting used letters in word_dictionary
            # that are also the same letters in hand
            updated_freq = hand[a_letter] - word_dictionary[a_letter]
            # Only adds the key/value pair if value > 0
            if updated_freq > 0:
                updated_hand[a_letter] = updated_freq
        # Just adds the key/value pair that isn't used in word_dictionary
        else:
            updated_hand[a_letter] = hand[a_letter]

    return updated_hand


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    # Create copy of word with all letters in small caps
    lowercase_word = word.lower()   
    # Use deep copy to actually make a copy instead of only referencing to 
    # same dictionary of hand variable(dictionary)
    hand_copy = copy.deepcopy(hand)
    possible_words = 0   

    used_wildcard = lowercase_word.find('*')
    # Cheks if '*' has been used. If used_wildcard's value isn't -1
    if used_wildcard >= 0:
        # Loop through the letters in VOWELS to check if there are possible valid words
        # created when replacing a wildcard character with a vowel letter
        for i in VOWELS:            
            # Replace wildcard character('*') with a letter in VOWELS (using index i)
            # and store it in test_word
            test_word = lowercase_word.replace(lowercase_word[used_wildcard], i)
            if test_word in word_list:
                possible_words += 1
                
        # Checks if any possible words exist from those vowels
        if possible_words > 0:
            return True
        else:
            return False
                  
    # Check if word(in lowercase) is in word_list
    elif lowercase_word in word_list:
        # Loops to check if all letters in lowercase_word are also in hand_copy
        for letter in lowercase_word:
            if letter not in hand_copy:
                return False            
            else:
                hand_copy[letter] -= 1
                if hand_copy[letter] == 0: # Removes key if value is 0 or less
                    del hand_copy[letter]                   

        return True
    
    else:
        return False


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    length = 0
    for i in hand:
        length += hand[i]

    return length

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    the_hand = hand
    print()

    total_score = 0
    while calculate_handlen(the_hand) > 0:
        print('Current Hand: ', end='')
        display_hand(the_hand)
        word = input('Enter word, or "!!" to indicate that you are finished: ')

        if word == '!!':
            break
        
        word_validation = is_valid_word(word, the_hand, word_list)
        if word_validation == True:
            word_score = get_word_score(word, calculate_handlen(the_hand))
            total_score += word_score
            print("\"" + word + "\"", 'earned', word_score,
                  'points. Total:', total_score, 'points')
            the_hand = update_hand(the_hand, word)
        else:
            print('That is not a valid word. Please choose another word.')
            the_hand = update_hand(the_hand, word)

        print()

    if word == '!!':
        print()
        print('Total score:', total_score, 'points')
    else:
        print()
        print('Ran out of letters. Total score:', total_score, 'points.')

    return total_score
        
 
    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    
        # Display the hand
        
        # Ask user for input
        
        # If the input is two exclamation points:
        
            # End the game (break out of the loop)

            
        # Otherwise (the input is not two exclamation points):

            # If the word is valid:

                # Tell the user how many points the word earned,
                # and the updated total score

            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                
            # update the user's hand by removing the letters of their inputted word
            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function



#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    hand_copy = copy.deepcopy(hand)        
    alphabet = VOWELS + CONSONANTS
    new_letter = random.choice(alphabet)

    # Loops until a random letter that isn't in the keys of the hand is found
    while new_letter in hand:
        new_letter = random.choice(alphabet)

    # Replaces the chosen key with random new_letter key 
    hand_copy[new_letter] = hand_copy[letter]
    del hand_copy[letter]

    return hand_copy
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    print()
    num_hands = int(input('Enter total number of hands: '))
    print()
    hand_substituted = False
    replay_hand = False
    looped = False
    replay_played = False

    over_all_score = 0
    score_array = []

    for i in range(num_hands):
        hand = deal_hand(HAND_SIZE)
        print('Current hand: ', end = '')
        display_hand(hand)
        
        if hand_substituted == False:
            substitute = input('Would you like to substitute a letter? ' )
            if substitute.lower() == 'yes':
                this_letter = input('Which letter would you like to replace? ')
                hand = substitute_hand(hand, this_letter)
                old_hand = copy.deepcopy(hand)
                hand_substituted = True            
        
        if looped == True and replay_hand == False:
            replay = input('Would you like to replay the hand? ')
            if replay.lower() == 'yes':
                hand = copy.deepcopy(old_hand)
                h = i - 1
                replay_hand = True
              
        hand_score = play_hand(hand, word_list)        
        score_array.append(hand_score)            
        
        old_hand = copy.deepcopy(hand)
        looped = True       
        
        print('----------')

    score_array.remove(score_array[h+1]) if score_array[h] > score_array[h+1] else score_array.remove(score_array[h])

    for i in score_array:
        over_all_score += i
    
    print('Total score over all hands:', over_all_score)

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#

if __name__ == "__main__":
          word_list = load_words()
          play_game(word_list)
