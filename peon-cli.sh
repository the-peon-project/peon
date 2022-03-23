#!/bin/bash
target=1000
while [ $target -ne '0' ]
do
	#clear
	invalid=true
	count=1
	#target_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/connector/"
	target_path=`echo "${BASH_SOURCE}" | rev | cut -d/ -f2- | rev`/cli/
	printf " ------ Peon CLI -------\n Please make a selection\n -----------------------\n"
	target_list=$(ls "$target_path")
	targets=()
	for script in $target_list
	do 
		printf " $count. ${script%".sh"}\n"
		((count=count+1))
	done
	printf " -----------------------\n 0. exit\n\n"
	printf " Selection: "
	read target
	if [[ $target =~ [^[:digit:]] ]]; then target=1000; fi # If not exlusively a digit then set to unused digit
	if [ "$target" -eq 0 ]; then exit 0; fi # If ZERO, exit
	if [ "$target" -ge 1 ] && [ "$target" -le $count ]; then invalid=false;fi # If digit & in the range that exists tell program that it is a valid entry.
	if $invalid
	then
	    printf "Invalid entry. Please try again"
	    read 
	    target=1000
	else
		count=1
		for script in $target_list
		do
			if [ $count -eq $target ]
			then
                printf " -----------------------\n      -- ${script%".sh"} --\n -----------------------\n\n"
				"$target_path"$script
				exit 0
			fi
			((count=count+1))
		done
	fi
done
exit 0

