import subprocess
import numpy as np
import os 

from src.signup import sign_up
from src.utils import retrain_users

def list_users(server_name: str):
    """
    Function to list the users and their roles
    
    Parameters
    ----------
    server_name : str
        The server_name from which to obtain the users
    """
    os.system('clear')
    
    users_list = retrain_users(server_name)
    
    # Print the users
    print("\n", "Username", "Role", sep="\t")
    for user, role in users_list:
        print("", user, role, sep="\t")
        
def delete_user(server_name: str, username:str):
    """
    Function to remove a user from the specified server_name

    Parameters
    ----------
    server_name : str
        The server_name from which to remove the user
    username : str
        The admin's username
    """
    os.system('clear')
    
    user = input("\tInsert the username to remove: ")
    
    cmd_rm = f"./mc admin user rm {server_name} {user}".split()
    subprocess.run(cmd_rm, capture_output=True)
    
    if user == username:
        print(f"You are no longer an user, exit")
        exit()

def update_user(server_name: str, username:str):
    """
    Update the policy of a user on the server_name.

    Parameters
    ----------
    server_name : str
        The server_name from which to remove the user
    username : str
        The admin's username
    """
    os.system('clear')
    
    # retrain the users' list
    users_list = retrain_users(server_name)

    user = input("\tInsert the username to change policy: ")
    user_idx = np.where(users_list[:, 0] == user)[0]
    # Check if the user exists
    if len(user_idx) > 0:      
        # Check the current policy
        current_policy = users_list[user_idx, 1][0]         
        new_policy     = "readwrite" if users_list[user_idx, 1] == "consoleAdmin" else "consoleAdmin"
            
        # Remove the previous policy and add the new one
        cmd_attach = f"./mc admin policy attach {server_name} {new_policy} --user {user}".split()
        cmd_detach = f"./mc admin policy detach {server_name} {current_policy} --user {user}".split()
        subprocess.run(cmd_attach, capture_output=True)
        subprocess.run(cmd_detach, capture_output=True)

        print(f"\tUser's policy changed from {current_policy} to {new_policy}")
        
        if user == username:
            print(f"You are no longer an admin, exit")
            exit()
    # Communicate if the user doesn't exist
    else:
        print("\tNot found")
        
def admin(username: str):
    """
    Function which provide a menu to the admin and allow to manage the users
    
    Parameters
    ----------
    username : str
        The admin's username
    """
    os.system('clear')
    server_name = "server_name"
        
    # Show the menu while the user wants to do some operations
    while True:
        operation = input("\nWhat operation do you want to do?\n" 
                        + "1 - List the users\n"
                        + "2 - Add a user\n"
                        + "3 - Delete a user\n"
                        + "4 - Change the user's policy\n"
                        + "5 - Log-out\n"
                        + "Response: ")
        
        # If the admin wants to list the users
        if operation == "1":
            list_users(server_name)
        
        # If the admin wants to add a new user    
        elif operation == "2":
            sign_up(is_admin=True)
            
        # If the admin wants to remove an existing user
        elif operation == "3":
            delete_user(server_name, username)
            
        # If the admin wants to change the policy to an existing user
        elif operation == "4":
            update_user(server_name, username)
                
        # If the admin wants to quit
        elif operation == "5":
            print("Have a nice day!!")
            break
        
        # If the admin command doesn't exist
        else: 
            print("Not valid")
