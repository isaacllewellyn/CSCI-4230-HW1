#TOY-DES ENCRPYTION
import sys
print(len(sys.argv))
import fileinput

#Static Data
Perm10             = ( 3, 5, 2, 7, 4, 10, 1, 9, 8, 6 )
Perm8              = ( 6, 3, 7, 4, 8, 5, 10, 9 )
Perm4              = ( 2, 4, 3, 1 )
InitialPermutation = ( 2, 6, 3, 1, 4, 8, 5, 7 )
InverseIP          = ( 4, 1, 3, 5, 7, 2, 8, 6 )
SBox0              = [ [1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2] ]
SBox1              = [ [0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3] ]
Key                = int('1100011110', 2)

Expand4to8         = ( 4, 1, 2, 3, 2, 3, 4, 1 )
#Functions
#Used to take a 4 bit input and reduce to 2 bits
def GetSbox(input, SBox):
    print("SBOX input: ", input)
    row = int( input[0] + input[3] , 2)#Take the first and last bits for the row
    column = int( input[1] + input[2] , 2)#Take the middle two for the column.
    print("SBOX output: ", '{0:02b}'.format(SBox[row][column]))# Format to 2 bit format
    return '{0:02b}'.format(SBox[row][column])#bin(SBox[row][column])[2:]

#Gets the left half of file
def LeftHalf(file):
    # print(int(len(file)/2))
    return file[:int(len(file)/2)]

#Gets the right half of file
def RightHalf(file):
    return file[int(len(file)/2):]

#Permutes file based on PermutationTable
def Permutation(file, PermutationTable):
    #Start Permutation on data based on PermutationTable
    result = ""
    for i in PermutationTable:# For each entry on the permutation table, we get a postition for our bit.
        result = result + (file[i-1])
    return result #Return the modified entry

#Shifts the file one to the left
def Shift(file):
    return file[1:] + file[0]#Take the second and rest elements, and append the first to the end

#Xor function, replaces bin(int((bits), 2) ^ int(Left, 2))[2:].rjust(8, '0'), as it sometimes gives bad values
def xor(bits, key):#Sometimes the python xor operator ( ^ ) does not work. This is a quick fix
    new = ''#Start with empty variable
    for bit, key_bit in zip(bits, key):#zip lets us iterate over two things at once
        new += str(((int(bit) + int(key_bit)) % 2))#by adding and taking the modulus, we preform an xor
    return new#return the string of binary

#Fiestiel function as described in lecture
def Fiest(bits, k1):
    #Split into two halves
    Left = LeftHalf(bits)
    Right = RightHalf(bits)
    #Expand the right to 8 bits
    bits = Permutation(Right, Expand4to8)
    #Xor the expanded bits with k1
    bits =  bin(int((bits), 2) ^ int(k1, 2))[2:].rjust(8, '0')
    #Reduce the bitspace via Sboxes
    bits = GetSbox(LeftHalf(bits), SBox0) + GetSbox(RightHalf(bits), SBox1)
    #Permute with P4
    bits = Permutation(bits, Perm4)
    #F end with xor of the left half with the output of feist
    print("Bits: ", bits, " Left: ", Left)
    #Return the xor of the two
    return  xor(bits, Left) #bin(int((bits), 2) ^ int(Left, 2))[2:].rjust(8, '0')

def SimpleDecrypt(file, k1, k2):
    # print("Starting Decryption")
    bits = Permutation(file, InitialPermutation) #Step one is to apply the IP array
    temp = Fiest(bits, k2)  #Run the first iteration of Fiestel with K2
    bits = RightHalf(bits) + temp #Flip the left and right
    bits = Fiest(bits, k1)        #Run the second iteration with K1
    return Permutation(bits+temp, InverseIP) #Lastly, run the InverseIP and return the decrypted textx

#encryptes 8 bit blocks
def SimpleEncrypt(file, k1, k2):
    #Split into 8 bit block
    #debug
    # bytes = int('00101000',2)
    bytes = file[0]
    #check file type
    print("Type bytes:", type(bytes))
    # print("Bytes:", bin(bytes)[2:].rjust(8, '0'))#rjust helps us avoid smaller bytes
    ib = bin(bytes)[2:].rjust(8, '0')#8 bytes here, if not 8 bits, makes 0 buffer
    bits = Permutation(ib, InitialPermutation) #Run the first permutation
    temp = Fiest(bits, k1)                     #Run Fiestel with K1
    bits = RightHalf(bits) + temp                   #Swap left and right
    bits = Fiest(bits, k2)                          #Run Fiestel with K2
    return (Permutation(bits + temp, InverseIP))    #Return cipher after InverseIP

#Converts a string of bits to a bytestring. Used to read the bitstrings
def bitstring_to_bytes(s):
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')#Used to convert binary strings to bytestrings

#Main Program
###Key generation
#initial Permutation of bit positions
#Steps are done following code diagram

k1aa = Permutation(bin(Key)[2:], Perm10) #Permutation(Shift(Permutation(bin(Key)[2:], Perm10)),Perm8)
k1a = Shift(LeftHalf(k1aa))
k1b = Shift(RightHalf(k1aa))
k1 = k1a + k1b
k1 = Permutation(k1,Perm8)
k2aa = (Permutation(bin(Key)[2:], Perm10))
k2a =   Shift(Shift(Shift(LeftHalf(k2aa))))#Permutation(Shift(Shift(Permutation(bin(Key)[2:], Perm10))),Perm8)
k2b =   Shift(Shift(Shift(RightHalf(k2aa))))
k2 = k2a + k2b
k2 = Permutation(k2, Perm8)
# K1 is P8(Shift(P10(K))
# K2 is P8(Shift(Shift(shift(p10(k))
####Key generation Complete
print("K1: ", (k1))
print("K2: ", (k2))
#check argument length
if(len(sys.argv)!=2):
    print("Error, needs to have one file argument")
else:
    check = sys.argv[1][-4:]
    if(check != "tdes"):
        print("Encrypting " + sys.argv[1] + " to " + sys.argv[1] + ".tdes")
        print("Starting loop")
        #load in file ## https://stackoverflow.com/questions/6787233/python-how-to-read-bytes-from-file-and-save-it
        in_file = open(sys.argv[1], "rb")  # opening for [r]eading as [b]inary
        file = in_file.read(1)
        efile = ""
        while file:
            #TODO stuff
            # if(len(file)<7):
            #     print("Filelength is too low, add some buffer!")
                #do that
            efile = efile + SimpleEncrypt(file, k1, k2)
            file = in_file.read(1)
        in_file.close()
        ####Begin Encrpytion of file
        # file = SimpleEncrypt(file, k1, k2)
        print("Encrypted file : ", efile)
        new_file = open( sys.argv[1]+".tdes" ,mode="w")

        new_file.write(efile)
        print("Encryption Done! Thank you for choosing Simple Encrypt! ", bitstring_to_bytes(efile))
    else:
        print("Decrypting....\n\n\n\n")
        dfile = ""
        # encfile = open(sys.argv[1] "rb")

        with open(sys.argv[1], "rb") as text_file:
            for line in text_file:
                line = line.decode('utf-8')#remove bytes from file nicely as python likes to wrap the bytes like so:  b'%bytes'
                # print("type:" ,type(line))

        efile = line
        print("Efille: ", int(efile,2))
        while len(efile) > 7:
            filepart = efile[0:8]
            dfile += SimpleDecrypt(filepart, k1, k2)
            file = SimpleDecrypt(dfile, k1, k2)
            efile = efile[8:]

        print("Decrypted file : ", dfile,  "\n Thank you for choosing Simple Encrypt")
        new_file = open(sys.argv[1][0:-5], mode="w")#remove ".tdes"
        mang0 = bitstring_to_bytes(dfile)
        print("Bytes: ", mang0)
        new_file.write(mang0.decode('utf-8'))                       #write to file
