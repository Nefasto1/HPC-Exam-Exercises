import subprocess
import numpy as np
from minio import Minio
import os

from admin import admin
from regular import regular

def retrain_users(server_name: str) -> np.array:
    """
    Function which returns the list of users and their roles
    
    Parameters
    ----------
    server_name : str
        The server_name from which to obtain the users
        
    Returns
    -------
    users_list: str-np.array
        Array containing the the users list and their roles
    """
    # minio mc bash command to list the users of the specified server_name
    cmd_list = f"./mc admin user list {server_name}".split()
    users_list = subprocess.run(cmd_list, stdout=subprocess.PIPE).stdout.decode("utf-8")
    users_list = users_list.split("\n")[:-1]
    users_list = [user.split()[1:] for user in users_list]
        
    return np.array(users_list)

def login():
    """
    Function to login to the cloud storage
    """
    server_name = "server_name"    
    
    # Retrain the users list
    users_list = retrain_users(server_name)
    
    if len(users_list) > 0:
        user_idx = []
        tries    = 0
        
        # Ask for the credential while the username or password are wrong
        print("\nLogin:")
        while len(user_idx) == 0:
            access = input("\tInsert the Username (0 to exit): ")
            if access == "0":
                exit()
                
            secret = input("\tInsert the Password (0 to exit): ")
            if secret == "0":
                exit()
            os.system('clear')
            
            # Try to access to the cloud storage
            client = Minio("127.0.0.1:9000",
                access_key=access,
                secret_key=secret,
                secure=False
            )
            
            # Check the user's role
            try: 
                found = client.bucket_exists(access)
                if not found:
                    client.make_bucket(access)
                user_idx = np.where(users_list[:, 0] == access)[0]
            except:
                user_idx = []
                
            if len(user_idx) == 0:
                print("\tUsername or password incorrect, retry")
                tries += 1
                
            if tries == 3:
                print("\tTo many attempt, closing")
                exit()
                
        role = users_list[user_idx, 1][0]
                        
        # Select the correct user's menu
        if role == "consoleAdmin":
            admin(access)
            exit()
        else:
            regular(client, access)
            exit()
            
    print("No users available")
