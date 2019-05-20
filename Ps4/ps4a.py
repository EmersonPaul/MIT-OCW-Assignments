# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    if len(sequence) == 1:
        return [sequence]
    
    permutation_list = []
    for letter in sequence:
        index = sequence.index(letter)
        for char in get_permutations(sequence[:index] + sequence[index + 1:]):
            permutation_list += [letter + char]

    return permutation_list

def string_permutation(string):
    if len(string) == 1 or len(string) == 0:
        return 1
    return len(string) * string_permutation(string[1:])
    

if __name__ == '__main__':
    
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    test_data = ['abc', 'bust', 'cd', 'rusty']

    for data in test_data:
        permutation_list = get_permutations(data)
        print('The permutations are   : ', permutation_list)
        print('Expected length of list: ', string_permutation(data))
        print('Actual length          : ', len(permutation_list))



