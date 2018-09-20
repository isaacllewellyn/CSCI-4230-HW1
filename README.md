# CSCI-4230-HW1
Isaac Llewellyn
661582062

Crypto 1:

This program will implement TOY-DES as discussed in lecture.

From slides, this is defined as:

Simplified DES
• Educational purpose
• Works on 8-bit blocks and uses 10-bit key
• Only 2 rounds
• Consider that plaintext and ciphertext are known:
– Plaintext : p1, p2, …, p8
– Ciphertext: c1, c2, …, c8
– Key: k1, k2, …, k10
simplified encryption algorithm will produce 8 non-linear equations (combination of linear and non-linear equations) with 10 unknowns. Note that:
– Permutations (P10, P8, P4) are linear
– “xor” additions are linear
– Substitution boxes (S0 and S1) are non-linear!

The code followed close to the diagrams given to us.

Our code has a variable that should be known:
    "Key                = int('1100011110', 2)" can be changed to any key for encryption.
This key is used to generate k1 and k2 before being input to the Fiest Function.


Encryption:
    After a file is input, the program reads the file byte by byte and encrypts each byte in 8 bit blocks using our 10 bit key. This is done by taking the 8 bit chunk and breaking into two halves. The right half goes into the Fiest function, which then gets expanded into 8 bits. Then the 8 bits get xored with K1. These 8 bits are reduced to 4 bits via two Substitution Boxes. This process splits the 8 bits in half, and uses the first and last bit from the halve to get the column, and the middle two bits to get the row in order to read the value of their respective S-Box. Once the bits are reduced, they are permutated again. Then these bits are xored with the left bits and passed out of the Fiest function. Now, the right half of bits are encrypted. The program then swaps left and right halves, and runs the Fiest function on the right halve with K2. Then, the bytes are added to a buffer which is in turn written to $filename.tdes for easy transfering between computers. After completing, the program then runs an inverse permutation on the bits to yield the cipher.
   
   
Decryption:
    The same steps as encryption are followed, however K2 is subsituted with K1 and visa-versa.

Usage: "main.py $file_to_encrypt_or_decrypt"


Output:
    - file.txt     -->  file.txt.tdes
    - file.txt.des -->  file.txt

When you input a file which is already encrypted by this program, it will automatically decrypt the cipher text into the original data. Any other file will be encrypted. 

Notes: This program does not check to see if a valid bytestream is in place. If not, unexpected results are sure to follow.
The speed of this program is heavily impacted by print statements. Removing all of them will increase efficiency.
Having a 10 bit key is not the most secure in practice, there are only 2^10 combinations of keys which can easily be brute forced by many computers let alone other types of attacks on the underlying crypto. As such, it should not be used for any important data.
