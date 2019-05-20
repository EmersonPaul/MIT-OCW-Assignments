from ps4b import *
import Testbox3

word_array = ['jell', 'get', 'type','cat','write','boy','girl', 'delicate']
decode = []

for word in word_array:
    x = Message(word)
    print('EXPECTED: ', Testbox3.invoke_shift(3, word))
    print('GOT:      ', x.apply_shift(3))
    decode.append(x.apply_shift(3))
    
print()
print('-------------')
print()

i = 0
for word in decode:
    y = CiphertextMessage(word)
    print('EXPECTED: ', word_array[i])
    print('GOT:      ', y.decrypt_message())
    i += 1
    
print()
print('-------------')
print()

z = PlaintextMessage('delicate', 3)
print(z.get_shift())
print(z.get_encryption_dict())
enc = z.get_message_text_encrypted()
dec = CiphertextMessage(enc)
print(enc)
print('expected text: delicate')
print('          got:', dec.decrypt_message())
z.change_shift(4)
print(z.get_shift())
print(z.get_encryption_dict())
enc = z.get_message_text_encrypted()
dec = CiphertextMessage(enc)
print(enc)
print('expected text: delicate')
print('          got:', dec.decrypt_message())
