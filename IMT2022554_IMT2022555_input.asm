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
