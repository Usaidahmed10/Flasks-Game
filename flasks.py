'''
Magical Flask Game
Written by : Usaid Ahmed
'''

import time
from bqueue import BoundedQueue
from bstack import BoundedStack
import os 
UNITS_OF_EACH_CHEMICAL = 3
LEVEL_FILES = ["chemicals1.txt", "chemicals2.txt", "chemicals3.txt"]  # List of levels
ANSI = {"AA": "\033[41m","BB": "\033[44m","CC": "\033[42m","DD": "\033[48;5;202m","EE": "\033[43m","FF": "\033[45m","RED": "\033[31m","GREEN": "\033[32m","UNDERLINE": "\033[4m","RESET": "\033[0m",
"CLEARLINE": "\033[0K"}  #dictionary for ANSI codes

def read_file(filename):
    '''
    Reads data from a file and returns it
    Inputs:
        filename (str): Name of the file to be read
    Returns:
        tuple: A tuple containing data read from the file (excluding the header), 
               the number of flasks, and the number of chemicals.
    '''    
    with open(filename,"r") as file:
        data = file.read().splitlines()
    num_of_flasks, num_of_chemicals = data[0].split()  # Extracting numbers of flasks and chemicals
    return data[1:], int(num_of_flasks), int(num_of_chemicals)

def display_header():
    """
    Displays an attractive header for the game.
    """
    clear_screen()
    print(ANSI["UNDERLINE"] + ANSI["GREEN"] + "🔥 Welcome to the Magical Flask Challenge! 🔥" + ANSI["RESET"])
    # print("Sort the chemicals into their flasks as quickly as you can!")
    # print("⏳ The clock is ticking! Show your skills and beat the time! ⏳")
    # print()

def create_flasks(num_of_flasks):
    '''
    Creates a list of flask objects based on the given number of flasks.
    Inputs:
        num_of_flasks (int): Number of flasks to be created.
    Returns:
        list: A list containing flask objects.
    '''    
    flasks = []
    for i in range(num_of_flasks):
        flasks.append(BoundedStack(4))  # Creating flask objects with a capacity of 4  
    return flasks

def fill_flask(queue, flasks, flask_num, quantity):
    '''
    Fills a specified flask with chemicals from a queue.    
    Inputs:
        queue (BoundedQueue): A queue containing chemicals.
        flasks (list): List of flask objects.
        flask_num (int): Index of the flask to be filled.
        quantity (int): Amount of chemical to fill. 
    Returns: N/A
    '''    
    for i in range(int(quantity)):
        flasks[int(flask_num)-1].push(queue.dequeue())

def flasks_setup(chemicals_data,flasks):
    '''
    Sets up the flasks with chemicals based on provided data.
    Inputs:
        chemicals_data (list): Data representing chemicals to be filled in flasks.
        flasks (list): List of flask objects. 
    Returns: N/A
    '''    
    queue = BoundedQueue(4)  # Creating a queue with a capacity of 4
    for item in chemicals_data:
        if len(item) > 2:
            quantity, flask_num = item.split("F")
            fill_flask(queue, flasks, flask_num, quantity)  # Filling the flasks with chemicals         
        else:
            if not queue.isFull():
                queue.enqueue(item)  # Enqueueing chemicals into the queue
                
def contents_of_flask(flask):
    '''
    Retrieves the contents of a flask.
    Inputs:
        flask (BoundedStack): A flask object.
    Returns:
        list: A list containing the contents of the flask.
    '''    
    contents = []
    if flask.size() > 0:
        for i in range(flask.size()):
            contents.insert(0, flask.pop())  # Popping and inserting contents into a list
            copy_contents = contents
        for chemical in copy_contents:
            flask.push(chemical)  # Pushing back the contents into the flask
    return contents
    
def is_sealed(flask):
    '''
    Checks if a flask is sealed, i.e., contains the same chemical thrice.
    Inputs:
        flask (BoundedStack): A flask object.
    Returns:
        bool: True if the flask is sealed, False otherwise.
    '''    
    if flask.size() == UNITS_OF_EACH_CHEMICAL:
        contents = contents_of_flask(flask)
        sealed = all(chemical == contents[0] for chemical in contents)  # Checking if all chemicals are identical
        return sealed
                
def pour(from_flask, to_flask):
    '''
    Transfers chemicals from one flask to another.
    Inputs:
        from_flask (BoundedStack): flask to pour from.
        to_flask (BoundedStack): flask to pour into.
    Returns: N/A
    '''    
    to_flask.push(from_flask.pop())  # Transferring chemicals between flasks
    
def print_flask_number(flask_num, from_flask, to_flask):
    '''
    Prints the flask number with color highlighting. 
    Inputs:
        flask_num (int): Index of the flask.
        from_flask (int): Index of the flask to pour from.
        to_flask (int): Index of the flask to pour into.
    Returns: N/A
    '''     
    if flask_num + 1 == from_flask:
        print(f"  {ANSI['RED']}{flask_num+1}{ANSI['RESET']}   ", end='')  # Highlighting flask number in red
    elif flask_num + 1 == to_flask:
        print(f"  {ANSI['GREEN']}{flask_num+1}{ANSI['RESET']}   ", end='')  # Highlighting flask number in green            
    else:
        print(f"  {flask_num+1}   ", end='')
    
    
    
def display_flasks(flasks, num_of_flasks, from_flask = 0, to_flask = 0):
    '''
    Displays the current state of all flasks.
    Inputs:
        flasks (list): List of flask objects.
        num_of_flasks (int): Total number of flasks.
        from_flask (int): Index of the flask to pour from (default is 0).
        to_flask (int): Index of the flask to pour into (default is 0).
    Returns: N/A
    '''    
    max_flasks_per_line = 4
    height_of_flasks = 4
    for i in range(0, num_of_flasks, max_flasks_per_line):
        for j in range(height_of_flasks, 0, -1):
            for k in range(i, min(i+max_flasks_per_line, num_of_flasks)):
                contents = contents_of_flask(flasks[k])
                if j-1 < len(contents):
                    print(f"|{ANSI[contents[j-1]]}{contents[j-1]}{ANSI['RESET']}|  ", end='')  # Displaying contents with color highlighting
                elif is_sealed(flasks[k]):
                    print("+--+  ", end='')  # displaying seal
                else:
                    print(f"|  |  ", end='')  # displaying empty portion 
            print() 
        print("+--+  "*min(max_flasks_per_line,num_of_flasks-i))
        for flask_num in range(i, min(i+max_flasks_per_line, num_of_flasks)):
            print_flask_number(flask_num, from_flask, to_flask)
        print()
        
def print_location(x, y, text):
    '''
    Prints text at the specified location on the terminal.
    Input:
        - x (int): row number
        - y (int): column number
        - text (str): text to print
    Returns: N/A
    '''
    print ("\033[{1};{0}H{2}".format(y,x, text))  # Printing text at specified coordinates
    
def move_cursor(x,y):
    '''
    Moves the cursor to the specified location on the terminal.
    Input:
        - x (int): row number
        - y (int): column number
    Returns: N/A
    '''
    print("\033[{1};{0}H".format(y,x), end='')  # Moving cursor to specified coordinates
    
def check_game_won(flasks):
    '''
    Checks if the game is won (all flasks contain the same chemical).
    Inputs:
        flasks (list): List of flask objects.
    Returns:
        bool: True if the game is won, False otherwise.
    '''    
    won = True
    for i in range(len(flasks)):
        if not is_sealed(flasks[i]) and len(contents_of_flask(flasks[i])) != 0:
            won = False
    return won  # If all flasks are either sealed or empty, the game is won
        
def from_flask_valid(from_flask, flasks):
    '''
    Validates the flask index from which pouring occurs.
    Inputs:
        from_flask (int): Index of the flask.
        flasks (list): List of flask objects.
    Returns:
        bool: True if the flask index is valid, False otherwise.
    '''    
    if from_flask.isdigit():  # Checking if the input is a digit and within the valid range of flask indices
        if int(from_flask) not in range(1,len(flasks)+1):
            print_location(5,0,"Invalid Input. Try Again")
            return False
        elif is_sealed(flasks[int(from_flask)-1]) or flasks[int(from_flask)-1].size() == 0:
            print_location(5,0,"Cannot pour from that flask. Try again.")
            return False
    elif from_flask.lower() != "exit":  # Handling the case where the user inputs 'exit
        print_location(5,0,"Invalid Input. Try Again")
        return False          
    move_cursor(5,0)
    print(ANSI["CLEARLINE"])
    return True

def to_flask_valid(from_flask, to_flask, flasks):
    '''
    Validates the flask index to which pouring occurs.
    Inputs:
        from_flask (int): Index of the flask to pour from.
        to_flask (int): Index of the flask to pour into.
        flasks (list): List of flask objects.
    Returns:
        bool: True if the flask index is valid, False otherwise.
    '''    
    if to_flask.isdigit():  # Checking if the input is a digit and within the valid range of flask indices
        if int(to_flask) not in range(1,len(flasks)+1):
            print_location(5,0,"Invalid Input. Try Again")
            return False
        elif is_sealed(flasks[int(to_flask)-1]) or flasks[int(to_flask)-1].isFull():
            print_location(5,0,"Cannot pour into that flask. Try again.")
            return False
        elif from_flask == to_flask:
            print_location(5,0,"Cannot pour into the same flask. Try again.")
            return False
    elif to_flask.lower() != "exit":  # Handling the case where the user inputs 'exit
        print_location(5,0,"Invalid Input. Try Again")
        return False        
    move_cursor(5,0)
    print(ANSI["CLEARLINE"])        
    return True
        
def clear_screen():
    '''
    Clears the screen.
    Inputs: N/A
    Returns: N/A
    '''    
    os.system("") # Enables ANSI escape codes in terminal
    # Clears the terminal. What happens if this gets removed?
    if os.name == "nt": # for Windows
        os.system("cls")
    else: # for Mac/Linux
        os.system("clear")    
    
    
def main():
    """
    Controls the game flow.
    """
    level = 0  # Start with the first level
    game_won = False  # Flag to track if the game is won
    exit_game = False  # Flag to track if the user chooses to exit

    while level < len(LEVEL_FILES) and not exit_game:
        filename = LEVEL_FILES[level]
        chemicals_data, num_of_flasks, num_of_chemcicals = read_file(filename)
        flasks = create_flasks(num_of_flasks)
        flasks_setup(chemicals_data, flasks)

        display_header()  # Display the header at the start of each level
        start_time = time.time()  # Record the start time for the level

        user_input1 = 0
        user_input2 = 0

        while not game_won:
            print_location(3, 0, "Select source flask: ")
            print_location(4, 0, "Select destination flask: ")

            move_cursor(6, 0)
            display_flasks(flasks, num_of_flasks, int(user_input1), int(user_input2))

            move_cursor(3, 21)
            user_input1 = input()
            while not from_flask_valid(user_input1, flasks):
                move_cursor(3, 21)
                print(ANSI["CLEARLINE"])
                move_cursor(3, 21)
                user_input1 = input()
                move_cursor(5, 0)
                print(ANSI["CLEARLINE"])
            if user_input1.lower() != "exit":
                move_cursor(4, 26)
                user_input2 = input()
                while not to_flask_valid(user_input1, user_input2, flasks):
                    move_cursor(4, 26)
                    print(ANSI["CLEARLINE"])
                    move_cursor(4, 26)
                    user_input2 = input()
                    move_cursor(5, 0)
                    print(ANSI["CLEARLINE"])
                if user_input2.lower() != "exit":
                    pour(flasks[int(user_input1) - 1], flasks[int(user_input2) - 1])
                    game_won = check_game_won(flasks)
                else:
                    exit_game = True
                    break
            else:
                exit_game = True
                break

        if game_won:
            end_time = time.time()  # Record the end time for the level
            time_taken = end_time - start_time
            display_flasks(flasks, num_of_flasks, int(user_input1), int(user_input2))
            print(f"🎉 Level Completed! Time Taken: {time_taken:.2f} seconds 🎉")

            if level < len(LEVEL_FILES) - 1:
                next_level = input("Do you want to continue to the next level? (yes/no): ").strip().lower()
                if next_level == "yes":
                    level += 1
                    game_won = False  # Reset for the next level
                else:
                    exit_game = True
            else:
                print("Congratulations! You've completed all levels! 🏆")
                exit_game = True
        elif exit_game:
            clear_screen()
            print("Thanks for playing! See you next time! 👋")
            
if __name__ == '__main__':
    main()

