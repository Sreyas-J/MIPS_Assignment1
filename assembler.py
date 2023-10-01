import os

file_path = "assembly.txt"

# Open the file in read mode
with open(file_path, 'r') as file:
    # Read the contents of the file
    file_contents = file.read()

lines=file_contents.split("\n")
#print(instructions)

def decimal_to_binary(number, num_bits):
    # Convert the decimal number to binary
    binary_representation = bin(number)[2:]  # Remove '0b' prefix

    # Calculate the number of padding zeros needed
    padding_zeros = num_bits - len(binary_representation)

    # Add the necessary padding zeros to achieve the desired number of bits
    binary_with_padding = '0' * padding_zeros + binary_representation

    return binary_with_padding

instructions={
    "lui":decimal_to_binary(15,6),
    "ori":decimal_to_binary(13,6),
    "add":decimal_to_binary(0,6),
    #"beq":decimal_to_binary()
}

functions={
    "add":decimal_to_binary(32,6)
}

data=[]

variables={
    "$zero":decimal_to_binary(0,5),
    "$v0":decimal_to_binary(2,5),
    "$v1":decimal_to_binary(3,5),
    "$a0":decimal_to_binary(4,5),
    "$a1":decimal_to_binary(5,5),
    "$a2":decimal_to_binary(6,5),
    "$a3":decimal_to_binary(7,5),
           
    "$t0":decimal_to_binary(8,5),
    "$t1":decimal_to_binary(9,5),
    "$t2":decimal_to_binary(10,5),
    "$t3":decimal_to_binary(11,5),
    "$t4":decimal_to_binary(12,5),
    "$t5":decimal_to_binary(13,5),
    "$t6":decimal_to_binary(14,5),
    "$t7":decimal_to_binary(15,5),

    "$s0":decimal_to_binary(16,5),
    "$s1":decimal_to_binary(17,5),
    "$s2":decimal_to_binary(18,5),
    "$s3":decimal_to_binary(19,5),
    "$s4":decimal_to_binary(20,5),
    "$s5":decimal_to_binary(21,5),
    "$s6":decimal_to_binary(22,5),
    "$s7":decimal_to_binary(23,5),

    "$ra":decimal_to_binary(31,5)
}

for line in lines:
    word=line.split()
    print(word)
    if(len(word)!=0):

        if word[0]=="li" or (len(word)>1 and word[1]=="li"):
            var=word[1].split(",")
            data.append(instructions["lui"]+"00000"+variables[var[0]]+decimal_to_binary(0,16))

            data.append(instructions["ori"]+variables[var[0]]+variables[var[0]]+decimal_to_binary(int(var[1]),16))

        if word[0]=="move" or (len(word)>1 and word[1]=="move"):
            var=word[1].split(",")
            data.append(instructions["add"]+variables["$zero"]+variables[var[1]]+variables[var[0]]+"00000"+functions["add"])

        #if word[0]=="beq" or (len(word)>1 and word[1]=="beq"):


print(data)