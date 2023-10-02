import os

file_path = "assembly.txt"

instructions_begining=0

# Open the file in read mode
with open(file_path, 'r') as file:
    # Read the contents of the file
    file_contents = file.read()

lines=file_contents.split("\n")

pseudoCode={
    "li":["lui","ori"],
    "move":["add"],
    "mul":["mult","mflo"]        
}

def beqHelper(target,lineNo):
    shift=0
    for i in range(lineNo+1,len(lines)):
        words=lines[i].split()
        for word in words:
            if(word=="mul"):
                shift+=1
            if(word==target):
                return i-lineNo+shift

def jHelper(target):
    shift = 0
    for i in range(len(lines)):
        if len(lines[i])==0:
            shift-=1
        words = lines[i].split()
        for word in words:
            if word in pseudoCode.keys():
                shift=shift+len(pseudoCode[word])-1
            if(word==target):
                return i+shift

def decimal_to_binary(number, num_bits):
    # Convert the decimal number to binary
    binary_representation = bin(number)[2:]  # Remove '0b' prefix

    # Calculate the number of padding zeros needed
    padding_zeros = num_bits - len(binary_representation)

    # Add the necessary padding zeros to achieve the desired number of bits
    binary_with_padding = '0' * padding_zeros + binary_representation

    return binary_with_padding

instructions={
    "li":"li",
    "move":"move",
    "lui":decimal_to_binary(15,6),
    "ori":decimal_to_binary(13,6),
    "add":decimal_to_binary(0,6),
    "beq":decimal_to_binary(4,6),
    "mult":decimal_to_binary(0,6),
    "mflo":decimal_to_binary(0,6),
    "lw":decimal_to_binary(35,6),
    "sw":decimal_to_binary(43,6),
    "addi":decimal_to_binary(8,6),
    "j":decimal_to_binary(2,6),
    "sub":decimal_to_binary(0,6),
    "bgt":decimal_to_binary(7,6)
}

data=[]

variables={
    "$0":decimal_to_binary(0,5),

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

for j in range(len(lines)):
    words=lines[j].split()
    for i in range(len(words)):
        if words[i] in instructions:
            if words[i]=="li":
                var=words[i+1].split(",")
                data.append(instructions["lui"]+"00000"+variables[var[0]]+decimal_to_binary(0,16))

                data.append(instructions["ori"]+variables[var[0]]+variables[var[0]]+decimal_to_binary(int(var[1]),16))

            if words[i]=="move":
                var=words[i+1].split(",")
                data.append(instructions["add"]+variables["$0"]+variables[var[1]]+variables[var[0]]+"00000"+"010000")

            if words[i]=="beq":
                var=words[i+1].split(",")
                data.append(instructions["beq"]+variables[var[0]]+variables[var[1]]+decimal_to_binary(beqHelper(var[2]+":",j),16))

            if words[i]=="mul":
                data.append(instructions["mult"]+variables[var[0]]+variables[var[1]]+"0000000000011000")
                data.append(instructions["mflo"]+"0000000000"+variables[var[3]]+"00000010010")
            
            if words[i]=="add":
                var=words[i+1].split(",")
                data.append(instructions["add"]+variables[var[2]]+variables[var[1]]+variables[var[0]]+"00000"+"010000")

            if words[i]=="lw":
                var=words[i+1].split(",")
                data.append(instructions["lw"]+variables[var[1][2:-1]]+variables[var[0]]+decimal_to_binary(int(var[1][0:1]),16))

            if words[i]=="sw":
                var=words[i+1].split(",")
                data.append(instructions["sw"]+variables[var[1][2:-1]]+variables[var[0]]+decimal_to_binary(int(var[1][0:1]),16))
                
            if words[i]=="addi":
                var=words[i+1].split(",")
                data.append(instructions["addi"]+variables[var[1]]+variables[var[0]]+decimal_to_binary(int(var[2]),16))

            if words[i]=="j":
                #print(words[i+1],jHelper(words[i+1]+":"))
                data.append(instructions["j"]+decimal_to_binary(instructions_begining+jHelper(words[i+1]+":"),26))

            if words[i]=="sub":
                var=words[i+1].split(",")
                data.append(instructions["sub"]+variables[var[2]]+variables[var[1]]+variables[var[0]]+"00000"+"100010")

            # if words[i]=="subi":
            #     var=words[i+1].split(",")
            #     data.append(instructions["addi"]+variables[var[1]]+variables[var[0]]+decimal_to_binary(int(var[2]),16))

            if words[i]=="bgt":
                var=words[i+1].split(",")
                data.append(instructions["bgt"]+variables[var[0]]+variables[var[1]]+decimal_to_binary(beqHelper(var[2]+":",j),16))

print(data)