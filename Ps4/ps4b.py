# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
import copy

file_name = "words.txt"

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'


class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        if shift < 0 or shift > 26:
            print("Invalid shift value")
            return None
        
        # This is an array of alphabet cases so we treat each element as index 0
        # to index 25 instead of combining the 2 elements and having to keep track of
        # the index of 52 characters vvv This statement down here
        alphabet_case = [string.ascii_lowercase, string.ascii_uppercase]
        
        last_index = 25 # The last index of the alphabet length (26 - 1) because it starts with 0
        shift_dict = {} # The dict where we put the letters and its equivalent cipher value

        # Loops through each element in alphabet_case and then loop through the letters
        # of each case then shift to corresponding shift letter(lower or uppercase)
        for case in alphabet_case:
            for letter in case:
                shift_index = case.index(letter) + shift
                if shift_index > last_index:
                    shift_index = abs(shift_index - last_index) - 1
                shift_dict[letter] = case[shift_index]

        return shift_dict
        

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''

        if shift < 0 or shift > 26:
            print("Invalid shift value")
            return None

        special_characters = " !@#$%^&*()-_+={}[]|\:;'<>?,./\""
        shifted_text = ''
        cipher_map = self.build_shift_dict(shift)
        
        for i in self.message_text:
            if i not in special_characters:
                shifted_text += cipher_map[i]
            else:
                shifted_text += i

        return shifted_text
        
        
class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.valid_words = load_words(WORDLIST_FILENAME) # TO BE FILLED IN BY FILE NAME
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)
        

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        encryption_dict2 = copy.deepcopy(self.encryption_dict)
        return encryption_dict2

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        decrypted_val = ()
        
        if len(self.message_text.split(' ')) == 1:
            word_list = self.message_text
        word_temp = self.message_text # store original version of encrypted message
        word_list = self.message_text.split(' ')
        main_key = {}

        for word in word_list:
            self.message_text = word # This was done so that apply.shift method uses each word instead
            for i in range(26):
                decrypt_try = Message.apply_shift(self, 26 - i)
                if is_word(self.valid_words, decrypt_try):
                    # Turns the shift into a key and records the number of times the shift was used
                    main_key[i] = main_key.get(i, 0) + 1

        best_shift_value = 26 - max(main_key, key = main_key.get) # Uses the key that was used the most and subtract it to 26
        self.message_text = word_temp # Assign self.message_text back to original state(encrypted message)
        decoded_word = Message.apply_shift(self, best_shift_value)
        decrypted_val = (best_shift_value, decoded_word)
        
        return decrypted_val
        

if __name__ == '__main__':

    #Example test case (PlaintextMessage)
    print()
    plaintext = PlaintextMessage('hello', 2)
    print('---------------')
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    print('---------------')

    #Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())
    print('---------------')

    #TODO: WRITE YOUR TEST CASES HERE

    #TODO: best shift value and unencrypted story 
    
    story = get_story_string()
    decrypted_story = CiphertextMessage(story)
    print('Output: ', decrypted_story.decrypt_message())
        
