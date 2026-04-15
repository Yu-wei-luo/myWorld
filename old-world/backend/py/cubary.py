# 01001100 01101111 01110110 01100101

string = input("Enter a binary string: ")
b = ''.join(format(ord(char), '08b') for char in string)
b = b.replace("1", "■").replace("0", "□")
print(b)