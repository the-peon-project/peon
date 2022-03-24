#!/bin/bash
# do something in two()
menu_peon() {
    draw_menu_header $menu_size "$app_name" "P E O N   C O N T A I N E R S"
    printf " 1. Connect to Container\n"
    printf " 2. Start Containers\n"
    printf " 3. Restart Containers\n"
    printf " 4. Stop Containers\n"
    printf " 5. Update Containers\n"
    printf " 0. Main Menu\n\n"
    pause
}
