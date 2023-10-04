#run in linux terminal by java -jar Mars4_5.jar nc filename.asm(take inputs from console)

#system calls by MARS simulator:
#http://courses.missouristate.edu/kenvollmar/mars/help/syscallhelp.html
.data
	next_line: .asciiz "\n"
	inp_statement: .asciiz "Enter No. of integers to be taken as input: "
	inp_int_statement: .asciiz "Enter starting address of inputs(in decimal format): "
	out_int_statement: .asciiz "Enter starting address of outputs (in decimal format): "
	enter_int: .asciiz "Enter the integer: "	
.text
#input: N= how many numbers to sort should be entered from terminal. 
#It is stored in $t1
jal print_inp_statement	
jal input_int 
move $t1,$t4			

#input: X=The Starting address of input numbers (each 32bits) should be entered from
# terminal in decimal format. It is stored in $t2
jal print_inp_int_statement
jal input_int
move $t2,$t4

#input:Y= The Starting address of output numbers(each 32bits) should be entered
# from terminal in decimal. It is stored in $t3
jal print_out_int_statement
jal input_int
move $t3,$t4 

#input: The numbers to be sorted are now entered from terminal.
# They are stored in memory array whose starting address is given by $t2
move $t8,$t2
move $s7,$zero	#i = 0
loop1:  beq $s7,$t1,loop1end
	jal print_enter_int
	jal input_int
	sw $t4,0($t2)
	addi $t2,$t2,4
      	addi $s7,$s7,1
        j loop1      
loop1end: move $t2,$t8       
#############################################################
#Do not change any code above this line
#Occupied registers $t1,$t2,$t3. Don't use them in your sort function.
#############################################################
#function: should be written by students(sorting function)
#The below function adds 10 to the numbers. You have to replace this with
#your code
li $t4,0	# initialising counter(i) for loop as 0
move $t5,$t1	# copying value of N into t5
li $s2,4	# initialising s2=4 to multiply with 4 with ease

loopcopy:  beq $t4,$t5,loopcopyend		# if i==N break out of the loop(this copies all values of input array to output array)
           mul $s3,$t4,$s2			# s3 moves to the ith data element(s3=i*4)
           add $t7,$t2,$s3		# t7 is used to find the position of ith data in input array
           lw $t6,0($t7)		# t6=input[i]
           add $t7,$t3,$s3		# find the position of ith data in output array
           sw $t6,0($t7)		# output[i]=t6
           addi $t4,$t4,1		# increamenting i(loop counter)
	   j loopcopy			# jump back to the starting of loop
loopcopyend: addi $t9,$t1,1		# t9=N+1
addi $s5,$0,1				# initialising loopcounter(i=1)

loopa: beq $s5,$t9,loopaend		# starting loopa, breaks out of loop if i==N+1
      addi $s6,$0,1				# initialising loopcounter(J=1)
      sub $s7,$t9,$s5          # s7=N+1-i(to set max value of J in loopb)
      loopb: beq $s6,$s7,loopbend		# starting loopb, breaks out of loop if J==N+1-i
     	    mul $s3,$s6,$s2			# (s3=j*4) used to jump to the next data
     	    add $t7,$t3,$s3			# t7=position of Jth data in ouput array
     	    lw  $s1,0($t7)			# s1=output[J]
     	    subi $s3,$s3,4			# used to access output data in j-1
     	    add $t7,$t3,$s3			# t7=position of (J-1)th data in output array
     	    lw $s4,0($t7)		# s4=output[J-1]
     	    
     	    bgt $s1,$s4,cond		# if output[J]>output[J-1], then skip swap function
     	    move $t4,$s1            # swaps the values of $s1 and $s4
     	    move $s1,$s4            # where $t4 is a temporary variable
     	    move $s4,$t4
     	    add $t7,$t3,$s3   		# $s4 is stored in its output array
     	    sw $s4,0($t7)
     	          
     	    addi $s3,$s3,4          # used to access output data in J+1
     	    add $t7,$t3,$s3			# $s1 is stored in its output array
            sw $s1,0($t7)
     	    cond: addi $s6,$s6,1 	# J is incremented by one
     	    	  j loopb
     	    
     loopbend: addi $s5,$s5,1 
     		j loopa 		# loopa is repeated
     
loopaend: 

#endfunction
#############################################################
#You need not change any code below this line

#print sorted numbers
move $s7,$zero	#i = 0
loop: beq $s7,$t1,end
      lw $t4,0($t3)
      jal print_int
      jal print_line
      addi $t3,$t3,4
      addi $s7,$s7,1
      j loop 
#end
end:  li $v0,10
      syscall
#input from command line(takes input and stores it in $t6)
input_int: li $v0,5
	   syscall
	   move $t4,$v0
	   jr $ra
#print integer(prints the value of $t6 )
print_int: li $v0,1	
	   move $a0,$t4
	   syscall
	   jr $ra
#print nextline
print_line:li $v0,4
	   la $a0,next_line
	   syscall
	   jr $ra

#print number of inputs statement
print_inp_statement: li $v0,4
		la $a0,inp_statement
		syscall 
		jr $ra
#print input address statement
print_inp_int_statement: li $v0,4
		la $a0,inp_int_statement
		syscall 
		jr $ra
#print output address statement
print_out_int_statement: li $v0,4
		la $a0,out_int_statement
		syscall 
		jr $ra
#print enter integer statement
print_enter_int: li $v0,4
		la $a0,enter_int
		syscall 
		jr $ra
