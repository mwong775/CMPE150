#!/bin/bash

# Write a shell script that only prints the even numbered lines of each file 
# in the current directory.
# Output should be filename: line for each even numbered line. (don't need line numbers).


for file in * ; 
	do 
	count=0
	while read i; 
		do
		isEven=$( expr $count % 2 )
		if [ $isEven -ne 0 ]
		then
			echo "$file: $i"
		fi
		(( count ++ ))
	done < $file

done 

