#!/bin/bash

menu_game (){
draw_menu_header $menu_size "$app_name" "G A M E   C O N T A I N E R S"
    printf " 1. Connect to Container\n"
    printf " 2. Start Container\n"
    printf " 3. Restart Container\n"
    printf " 4. Stop Container\n"
    printf " 0. Main Menu\n\n"
    pause
}