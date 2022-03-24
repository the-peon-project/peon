#!/bin/bash
source cli-v2/modules.sh
trap '' SIGINT SIGQUIT SIGTSTP
while true
do
	main_menu
	read_mm_options
done