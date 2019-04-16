# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()

def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    letter_included = False

    # Loops through secret_word and checks if each letter is in letters_guessed
    for a_letter in range(len(secret_word)):
        if secret_word[a_letter] in letters_guessed:
            letter_included = True
        else:
            letter_included = False
            break
    return letter_included            


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    combined_letters = []
    # same looping mechanism inside the is_word_guessed() function
    for a_letter in range(len(secret_word)):
        if secret_word[a_letter] in letters_guessed:
            combined_letters.append(secret_word[a_letter])
        else:
            combined_letters.append('_ ')
    combined_letters = "".join(combined_letters) # Turns list of letters to a string
    return combined_letters


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    lower_case_letters = string.ascii_lowercase
    lower_case_letters = list(lower_case_letters) # Converts ASCII lowercase letters(a string) to a list
    # Loop through the list of guessed letters and compare if they have been used in available letters
    for each_letter in range(len(letters_guessed)):
        if letters_guessed[each_letter] in lower_case_letters:
            lower_case_letters.remove(letters_guessed[each_letter]) # Remove letter if it is in letters_guessed list
    lower_case_letters = "".join(lower_case_letters) # Converts back to string 
    return lower_case_letters
        

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guesses = 6
    warning = 3    
    letters_guessed = []
    has_guessed = False
    vowels = 'aeiou' # Used to check for vowels and consonants
    unique_letter = [] # Stores unique letters to be used to be used for score later
    checker_index = 0 # Index of the loop that checks if letters are unique
    warnings_used = False
    for each_letter in range(len(secret_word)):
        current_letter = secret_word[each_letter] # Stores letter from the current index of 'secret_word'
        letter_counter = 0 # Reset the amount of multiple same letters found
        for checker_index in range(len(secret_word)):
            if current_letter == secret_word[checker_index]:
                letter_counter += 1
        if letter_counter == 1:
            unique_letter.append(current_letter)     

    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    while guesses > 0:
        print('-------------')
        print('You have', guesses, 'guesses left')
        print('Available letters:', get_available_letters(letters_guessed))
        letter_guess = input('Please guess a letter: ')
        letter_guess = letter_guess.lower()
        if letter_guess in secret_word and letter_guess not in letters_guessed:
            letters_guessed.append(letter_guess)
            print('Good guess:', get_guessed_word(secret_word, letters_guessed))
        elif letter_guess not in string.ascii_lowercase:
            warning -= 1
            print('Oops! That is not a valid letter! You have', warning, 'warnings left.',
                  get_guessed_word(secret_word, letters_guessed))
        elif letter_guess in letters_guessed:
            warning -= 1
            print("Oops! You've already guessed that letter! You have", warning, 'warnings left.',
                  get_guessed_word(secret_word, letters_guessed))
        elif len(letter_guess) > 1:
            warning -= 1
            print('Oops! You should only put one letter! You have', warning, 'warnings left.',
                  get_guessed_word(secret_word, letters_guessed))
        else:
            if letter_guess not in vowels and letter_guess not in secret_word:
                guesses -= 1
            elif letter_guess in vowels and letter_guess not in secret_word:
                guesses -= 2            
            letters_guessed.append(letter_guess)
            print('Oops! That letter is not in my word! You have', guesses, 'guesses left.',
                  get_guessed_word(secret_word, letters_guessed))
            
        if warning == 0:
            warnings_used = True
            if warnings_used == True:
                print("You've already used up all of your warnings! You lose 1 guess")
                guesses -= 1
                warnings_used = False # Returns to false so it doesn't keep executing prior 2 lines            
            
        # Checks if guessed letters are in the secret word
        has_guessed = is_word_guessed(secret_word, letters_guessed)
        if has_guessed == True:
            break

    if has_guessed == True:
        print('Congratulations, you won!')
        print('Your total score for this game is:', len(unique_letter) * guesses)
    else:
        print('Sorry, you ran out of guesses! The word was', '\'' + secret_word + '\'')    


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    secret_word = choose_word(wordlist)
    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)
