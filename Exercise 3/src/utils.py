import numpy as np
import subprocess

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