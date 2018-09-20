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

Usage: "main.py $file_to_encrypt_or_decrpyt"

Output:
    - file.txt     -->  file.txt.tdes
    - file.txt.des -->  file.txt

Notes: This program does not check to see if a valid bytestream is in place. If not, unexpected results are sure to follow.
The speed of this program is heavily impacted by print statements. Removing all of them will increase efficiency. k
