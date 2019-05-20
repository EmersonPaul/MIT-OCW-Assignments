import string

def shift_letter(shift):
    
    assert shift >= 0 and shift < 26
    
    alphabet_type = [string.ascii_lowercase, string.ascii_uppercase]
    last_index = len(string.ascii_lowercase) - 1
    shift_map = {}
    for case in alphabet_type:
        for letter in case:
            shift_index = case.index(letter) + shift
            if shift_index > last_index:
                shift_index = abs(shift_index - last_index) - 1
            shift_map[letter] = case[shift_index]
        
    return shift_map

def invoke_shift(shift, string):
    
    if shift < 0 or shift > 26:
        print("Invalid shift value")
        return None

    special_characters = " !@#$%^&*()-_+={}[]|\:;'<>?,./\""

    shifted_text = ''
    cipher_map = shift_letter(shift)
    
    for i in string:
        if i not in special_characters:
            shifted_text += cipher_map[i]
        else:
            shifted_text += i

    return shifted_text
