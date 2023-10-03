import os

file_path = "template.asm" #mips code is present here

instructions_begining=2**20 #start of addresses in data memory, used for jump statement

# Open the file in read mode
with open(file_path, 'r') as file:
    # Read the contents of the file
    file_contents = file.read()

lines=file_contents.split("\n") #splits mips code into lines


def decimal_to_binary(number, num_bits):# converts decimal numbers to binary with necessary number of bits
    # Convert the decimal number to binary
    binary_representation = bin(number)[2:]  # Remove '0b' prefix

    # Calculate the number of padding zeros needed
    padding_zeros = num_bits - len(binary_representation)

    # Add the necessary padding zeros to achieve the desired number of bits
    binary_with_padding = '0' * padding_zeros + binary_representation

    return binary_with_padding

pseudoCode={
    "li":["addiu"],
    "move":["addu"],   
    "subi":["addi","sub"],
    "bgt":["slt","bne"]
} #all the psuedo codes used

instructions={
    "li":"li",
    "move":"move",
    "subi":"subi",
    "bgt":"bgt",
    "addiu":decimal_to_binary(9,6),
    "addu":decimal_to_binary(0,6),
    "add":decimal_to_binary(0,6),
    "beq":decimal_to_binary(4,6),
    "mul":decimal_to_binary(28,6),
    "lw":decimal_to_binary(35,6),
    "sw":decimal_to_binary(43,6),
    "addi":decimal_to_binary(8,6),
    "j":decimal_to_binary(2,6),
    "sub":decimal_to_binary(0,6),
    "slt":decimal_to_binary(0,6),
    "bne":decimal_to_binary(5,6)
} #instructions with their opcodes

data=[] #machine code

variables={
    "$0":decimal_to_binary(0,5),
    "$1":decimal_to_binary(1,5),

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

    "$t8":decimal_to_binary(24,5),
    "$t9":decimal_to_binary(25,5),

    "$ra":decimal_to_binary(31,5)
} #registers in mips

def beqHelper(target,lineNo): #this function is used to calculate the offset in beq and slt instruction
    shift=0#checks for empty lines
    for i in range(lineNo+1,len(lines)):#offset is calculated from next line of beq until the target
        words=lines[i].split()
        if(len(words)==0):
            shift-=1
        for word in words:
            if word in pseudoCode.keys():#as psuedo codes may contain more than one instruction
                shift=shift+len(pseudoCode[word])-1
            if(word==target):
                return i-lineNo+shift-1 #final offset value

def jHelper(target): #this is used to calculate the addreses
    shift = 0 #empty lines
    for i in range(len(lines)):
        if len(lines[i])==0:
            shift-=1
        words = lines[i].split()
        for word in words: 
            if word == "#":
                break
            if word in pseudoCode.keys():#psuedo codes may contain more than one instruction
                shift=shift+len(pseudoCode[word])-1
            if(word==target):
                return i+shift #final address

for j in range(len(lines)): #main part of program, checks for the instructions and gives the machine code
    words=lines[j].split()#splits each line into a list of words
    for i in range(len(words)):#checks which word starts with the instructions
        if words[i] in instructions:
            #machine code is written depending on r,i,j format
            if(words[i]=="#"):
                break
            if words[i]=="li":
                var=words[i+1].split(",")#seperate the required arguements
                data.append(instructions["addiu"]+"00000"+variables[var[0]]+decimal_to_binary(int(var[1]),16))

            if words[i]=="move":
                var=words[i+1].split(",")
                data.append(instructions["addu"]+variables["$0"]+variables[var[1]]+variables[var[0]]+"00000"+"100001")

            if words[i]=="beq":
                var=words[i+1].split(",")
                data.append(instructions["beq"]+variables[var[0]]+variables[var[1]]+decimal_to_binary(beqHelper(var[2]+":",j),16))

            if words[i]=="mul":
                var=words[i+1].split(",")
                data.append(instructions["mul"]+variables[var[1]]+variables[var[2]]+variables[var[0]]+"00000"+"000010")
            
            if words[i]=="add":
                var=words[i+1].split(",")
                data.append(instructions["add"]+variables[var[1]]+variables[var[2]]+variables[var[0]]+"00000"+"100000")

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
                data.append(instructions["j"]+decimal_to_binary(instructions_begining+jHelper(words[i+1]+":"),26))

            if words[i]=="sub":
                var=words[i+1].split(",")
                data.append(instructions["sub"]+variables[var[1]]+variables[var[2]]+variables[var[0]]+"00000"+"100010")

            if words[i]=="bgt":
                var=words[i+1].split(",")
                data.append(instructions["slt"]+variables[var[1]]+variables[var[0]]+variables["$1"]+"00000"+"101010")
                data.append(instructions["bne"]+variables["$1"]+variables["$0"]+decimal_to_binary(beqHelper(var[2]+":",j),16))

            if words[i]=="subi":
                var=words[i+1].split(",")
                data.append(instructions["addi"]+variables["$0"]+variables["$1"]+decimal_to_binary(int(var[2]),16))
                data.append(instructions["sub"]+variables[var[1]]+variables["$1"]+variables[var[0]]+"00000"+"100010")

with open("output.txt", 'w') as file:
    for machine in data:
        file.write(str(machine) + '\n')