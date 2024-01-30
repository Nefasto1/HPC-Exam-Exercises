import numpy as np
from minio import Minio
import os

from src.admin import admin
from src.regular import regular
from src.utils import retrain_users

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
