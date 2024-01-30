from minio import Minio
import os

def list_bucket(client: Minio, bucket_name: str):
    """
    Function to list the user bucket
    
    Parameters
    ----------
    client: Minio-obj
        Client from where obtain the user's informations
    bucket_name: str
        Name of the user's bucket
    """
    os.system('clear')
    # Obtain the objects list
    objects = client.list_objects(bucket_name)

    # Print the list
    print("\tYour bucket content: ")    
    print("\t","| Name ", "| " + "Size", "| " + "Last Modified |", sep="\t")    
    print("\t", "-"*33 , sep="\t")    
    for o in objects:
        print("\t", "| " + o.object_name, "| " + str(o.size), "| " + str(o.last_modified)[:10], "|", sep="\t")
        
def add_object(client: Minio, bucket_name: str):
    """
    Function which upload the user's file into the bucket
    kes key create my-minio-sse-kms-key
    Parameters
    ----------
    client: Minio-obj
        Client from where obtain the user's informations
    bucket_name: str
        Name of the user's bucket
    """
    os.system('clear')
    
    # Define the elements to upload
    destination_file = input("\tInsert the name with which save the file: ")
    source_file      = input("\tInsert the file's path: ")
    
    # Insert them in the user's bucket
    client.fput_object(
        bucket_name, 
        destination_file, 
        source_file,
    )
    
    print(f"{source_file} successfully uploaded as object {destination_file} to bucket {bucket_name}")

def remove_object(client: Minio, bucket_name: str):
    """
    Function to remove a file from the user's bucket

    Parameters
    ----------
    client: Minio-obj
        Client from where obtain the user's informations
    bucket_name: str
        Name of the user's bucket
    """
    os.system('clear')
    # Select the object to remove
    name = input("\tInsert the name of the file to delete: ")
    
    # Remove it
    client.remove_object(bucket_name, name)
    
    print(f"{name} successfully removed from bucket {bucket_name}")
    
def download_object(client: Minio, bucket_name: str):
    """
    Function to download a file from the user's bucket

    Parameters
    ----------
    client: Minio-obj
        Client from where obtain the user's informations
    bucket_name: str
        Name of the user's bucket
    """
    os.system('clear')
    
    # Select the object to download and where
    destination_file = input("\tInsert the name with which save the file: ")
    downloaded_file = input("\tInsert the file's path: ")
    
    # Download it
    client.fget_object(
        bucket_name, 
        destination_file, 
        downloaded_file,
    )
    
    print(f"{destination_file} successfully downloaded as {downloaded_file} from bucket {bucket_name}")

def regular(client, bucket_name):
    """
    Function which provide a menu to the user and allow to manage the objects

    Parameters
    ----------
    client: Minio-obj
        Client from where obtain the user's informations
    bucket_name: str
        Name of the user's bucket
    """        
    os.system('clear')
    
    # Show the menu while the user wants to do some operations
    while True:
        operation = input("\nWhat operation do you want to do?\n" 
                        + "1 - List the files\n"
                        + "2 - Add a file\n"
                        + "3 - Delete a file\n"
                        + "4 - Download a file\n"
                        + "5 - Log-out\n"
                        + "Response: ")
        
        # If the regular wants to list the objects
        if operation == "1":        
            list_bucket(client, bucket_name)

        # If the regular wants to add an objects
        elif operation == "2":
            add_object(client, bucket_name)
            
        # If the regular wants to remove an objects
        elif operation == "3":
            remove_object(client, bucket_name)
    
        # If the regular wants to download an objects
        elif operation == "4":
            try:
                download_object(client, bucket_name)
            except:
                print("Errors on the download, check the file name or the path")
            
        # If the regular wants to quit
        elif operation == "5":
            print("Have a nice day!!")
            break
            
        # If the regular command doesn't exist
        else: 
            print("Not valid")
