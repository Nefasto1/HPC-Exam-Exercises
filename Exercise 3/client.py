from login import login
from signup import sign_up

import os

def login_menu():
    """
    Function to display the login menu
    """
    
    # Ask for operation while it is not valid
    choice = input("Choice how to access [login/register]: ")
    while choice not in ["login", "register", "l", "r"]:
        print("\nNot valid")
        choice = input("Choice how to access [login/register]: ")
    
    os.system('clear')
    # Select the asked operation
    if choice in ["login", "l"]:
        login()
    else:
        sign_up()
        
        os.system('clear')
        
        login()
        
if __name__ == "__main__":
    login_menu()