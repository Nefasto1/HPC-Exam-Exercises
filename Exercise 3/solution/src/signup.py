import subprocess
import os

from src.utils import retrain_users

def sign_up(is_admin: bool = False):
    """
    Function to signup to the cloud storage
    
    Parameters
    ----------
    is_admin: bool
        If true the user is being created by an admin
    """
    server_name = "server_name"
    
    # Retrain the users list
    users_list = retrain_users(server_name)

    # Ask for a username while is not valid
    print("\nSign up")
    while True:
        access = input("\tInsert the Username: ")
        os.system('clear')
        
        # If is ok exit the cycle
        if access not in users_list and len(access) >= 3 and len(access) <= 20:
            break
        elif not (len(access) >= 3 and len(access) <= 20):
            print("\tUsername length should be between 3 and 20")
        else:
            print("\tUsername already in use!!")
    
    # Ask for a username while is not valid
    while True:
        secret = input("\tInsert the Password: ")
        os.system('clear')
        
        # If is ok exit the cycle
        if len(secret) >= 8 and len(secret) < 40:
            break
        print("\tThe password length should be between 8 and 40")
    
    # If the user is created from an admin ask if the new user is an admin too
    admin = input("\tIs an Admin? [Y/n]: ") if is_admin else "n"
    
    # Assign the policy consistently with the choice
    policy = "consoleAdmin" if admin in ["Y", "y"] else "regular"
    
    # Create the user and assign the policy to him
    cmd_add = f"./mc admin user add {server_name} {access} {secret}".split()
    cmd_policy = f"./mc admin policy attach {server_name} {policy} --user {access}".split()
    subprocess.run(cmd_add, capture_output=True)
    subprocess.run(cmd_policy, capture_output=True)
    
    role = "admin" if admin in ["Y", "y"] else "regular"
    print(f"User {access} added successfully as {role} user")