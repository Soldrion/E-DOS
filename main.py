#remember to add the login system

from brython_graphics import *
from browser import timer
cursor = Rectangle(10, 20)
screen = []
textlist = []
x = 0
boole = [True] 
username = "chudbobsquarepants"
hostname = "EdPC"
command = ""
storage_devices = [None]
kernel_info = "0.0.1"
dosmode = False
global current_directory
current_directory = ""

#DIRECTORIES
dir_home = ["/home","sussy","baka"]
dir_lib = ["/lib"]
dir_bin = ["/bin"]
dir_tmp = ["/tmp"]
dir_etc = ["/etc"]
dir_root = ["/root"]
dir_mnt = ["/mnt"]
dir_boot = ["/boot"]
dir_opt = ["/opt"]
dir_usr_bin = []
dir_usr_local = []
dir_usr_include = []
dir_usr_sbin = []
dir_usr = ["/usr",dir_usr_bin,dir_usr_local,dir_usr_include,dir_usr_sbin]
global accepted_directories
directories = [dir_home[0],dir_lib[0],dir_bin[0],dir_tmp[0],dir_etc[0],dir_root[0],dir_mnt[0],dir_boot[0],dir_opt[0],dir_usr[0]]
accepted_directories = [dir_home,dir_lib,dir_bin,dir_tmp,dir_etc,dir_root,dir_mnt,dir_boot,dir_opt,dir_usr,dir_usr_bin,dir_usr_local,dir_usr_include,dir_usr_sbin]


flash_cursor_bool = False
command_list = ["ls","cd","pwd","mkdir","grep","exit","head","less","mv","sudo","tail","clear","dos_fdisk","dos_type","dos_edit","print","dir"]


screen_lines = ["Welcome to E-DOS","Kernel Version:"+kernel_info,"Storage Devices:"+str(storage_devices)]
screen_line_entities = []
def init_screen(): #initializes screen, uses screen list to push things into the screen 
    background = Rectangle(get_width(), get_height())
    add(background)

def draw_screen(): #draws everything in screen list
    global screen_line_entities
    global flash_cursor_bool
    for oldline in screen_line_entities:
        remove(oldline)
    screen_line_entities = []
    line_padding = get_height() - 20
    for line in reversed(screen_lines):
        linetext = Text(line)
        linetext.set_position(0, line_padding)
        linetext.set_color(Color.white)
        linetext.set_font("10pt Courier New")
        add(linetext)
        screen_line_entities.append(linetext)
        line_padding -= 10
    
    promptStr = f"{username}@{hostname}{current_directory}:{command}"
    prompt = Text(promptStr)
    prompt.set_color(Color.white)
    prompt.set_font("10pt Courier New")
    prompt.set_position(0, get_height()-10)
    add(prompt)
    screen_line_entities.append(prompt)
    
    if flash_cursor_bool:
        cursor = Rectangle(7, 15)
        cursor.set_position(len(promptStr) * 8, get_height()-22)
        cursor.set_color(Color.white)
        add(cursor)
        screen_line_entities.append(cursor)

def init_cursor(): #cursor stuff
    cursor.set_color(Color.white)
    cursor.set_position(((hostlen+userlen+signifierlen)*9), get_height() - 25)
    add(cursor)
def blink_cursor(boole): #cursor stuff
    if boole[0]:
        cursor.set_color(Color.white)
    else:
        cursor.set_color(Color.black)

def input_callback():
    key = e.key
    
def timer_to_blinker():
    boole[0] = not boole[0]
    blink_cursor(boole)
def input_handler(e):
    global command
    global flash_cursor_bool
    flash_cursor_bool = True
    if e.key not in ["ArrowLeft", "ArrowRight", "ArrowDown", "ArrowUp", "Control", "Alt", "Enter", "CapsLock", "Tab", "Shift","Backspace", "Meta","F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12"]:
        command += str(e.key)
    if e.key == "Backspace":
        command = command[:-1] 
    if e.key == "Enter":
        cmd_processor(command)
        command = command[:command] 
        
        
        
        # Control, Shift, CapsLock, Tab, `, Escape, Backspace, Enter, Alt 

def cmd_processor(cmd):
    global current_directory  
    comb_line = username + "@" + hostname + current_directory+":" + command
    screen_lines.append(comb_line)
    cmd_split = cmd.split(' ')
    if cmd == "dos_fdisk":
        screen_lines.append("the disk is f")
    items = []
    if cmd == "ls":
        screen_lines.append(" ")
        for i in range(0,len(directories)):
            item = directories[i] 
            items.append(item)
            if i == 8:
                items.append(" ")
                screen_lines.append(items)
                items = []
                screen_lines.append(items)
            if i == 16:
                items.append(" ")
                screen_lines.append(items)
                items = []
                screen_lines.append(items)
        screen_lines.append(" ")
    if cmd == "neofetch":
        screen_lines.append("package 'neofetch' not available")

    if cmd == "dir":
        screen_lines.append(directories)
    if cmd == "fwd":
        print()
    
    if cmd_split[0] == "man":
        items = []
        screen_lines.append(" ")
        screen_lines.append("MANUAL")
        screen_lines.append(" ")
        screen_lines.append("Commands:")
        for i in range(len(command_list)):
            item = command_list[i] 
            items.append(item)
            if i == 10:
                items.append(" ")
                screen_lines.append(items)
                items = []
                screen_lines.append(items)
                screen_lines.append(" ")
        screen_lines.append("Documentation:")
        screen_lines.append(" ")
        screen_lines.append("When in directories other than hostname@username,")
        screen_lines.append("The color of all text will be a different color.")
        screen_lines.append(" ")
        screen_lines.append("To use MS-DOS commands, use the 'dos_' prefix.")
        screen_lines.append(" ")

        
    if cmd_split[0] == "cd":
        target_directory = cmd_split[1]
        if cmd_split[1] == None:
            screeen_lines.append(cmd)
             
        found_directory = None
        for directory_list in accepted_directories:
            for directory in directory_list:
                if directory == target_directory:
                    found_directory = directory
                    break
        if found_directory:
            screen_lines.append("Current directory: " + found_directory)
            current_directory = found_directory
        else:
            screen_lines.append(f"Directory '{target_directory}' not found")

    if cmd_split[0] == "print":
        if cmd_split[1] == "accepted_directories":
            screen_lines.append(accepted_directories)
        elif cmd_split[1] == "cd":
            screen_lines.append(current_directory)
        else:
            screen_lines.append(cmd_split[1])
    if cmd_split[0] not in command_list:
        screen_lines.append("Command not found.")
        return

def kernel():
    init_screen()

timer_id = timer.set_interval(draw_screen, 350)

def flash_cursor():
    global flash_cursor_bool
    flash_cursor_bool = not flash_cursor_bool
timer.set_interval(flash_cursor, 500)
kernel()
add_key_down_handler(input_handler)
add_key_down_handler(input_callback)
