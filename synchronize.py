import os
import time
import shutil
import hashlib
import argparse
from datetime import datetime


def calculate_file_hash(file_path):
    """Calculates MD5 hash for a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def calculate_folder_hash(folder_path):
    """Calculates a combined hash for all files in the folder (and subfolders)."""
    folder_hash = hashlib.md5()  
    
    for dirpath, _, filenames in os.walk(folder_path):
        for file_name in sorted(filenames):  
            file_path = os.path.join(dirpath, file_name)
            file_hash = calculate_file_hash(file_path)  
            folder_hash.update(file_hash.encode())  
    
    return folder_hash.hexdigest()


def sync_folders(source_folder_path, replica_folder_path, log_file):
    """Synchronizes the replica folder with the source folder."""

    #Getting the names of files presents in the source folder
    files_names_source = os.listdir(source_folder_path)
    files_names_replica = os.listdir(replica_folder_path)
    files_names_replica_dup = files_names_replica.copy()

    for file in files_names_source:

        file_path = os.path.join(source_folder_path, file)
        new_file_path = os.path.join(replica_folder_path, file)
           
        if file not in files_names_replica:
                
            if os.path.exists(file_path):
                # If it's a folder
                if os.path.isdir(file_path):  
                    shutil.copytree(file_path, new_file_path)
                    
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_file.write(f"[{timestamp}] {file} and its contents were created in path {replica_folder_path}\n\n")
                    print(f"[{timestamp}] {file} and its contents were created in path {replica_folder_path}")
                
                # If it's a file
                else:  
                    shutil.copy2(file_path, new_file_path)
                    
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{timestamp}] {file} was created in path {replica_folder_path}")
                    log_file.write(f"[{timestamp}] {file} was created in path {replica_folder_path}\n\n")
                    
        elif file in files_names_replica:
            
            # If it's a folder
            if os.path.isdir(file_path):  
                hash_source = calculate_folder_hash(file_path)
                hash_replica = calculate_folder_hash(new_file_path)
                
                if hash_source != hash_replica:
                    sync_folders(file_path, new_file_path, log_file)
            
            # If it's a file
            else:
                size_source = os.path.getsize(file_path)
                size_replica = os.path.getsize(new_file_path)

                if size_source ==size_replica:
                    
                    hash_source = calculate_file_hash(file_path)
                    hash_replica = calculate_file_hash(new_file_path)
                    
                    if hash_source != hash_replica:
                        os.remove(new_file_path)
                        shutil.copy2(file_path, new_file_path)
                        
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"[{timestamp}] {file} was modified in path {replica_folder_path}")
                        log_file.write(f"[{timestamp}] {file} was modified in path {replica_folder_path}\n\n")  
                
                else:
                    os.remove(new_file_path)
                    shutil.copy2(file_path, new_file_path)
                    
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{timestamp}] {file} was modified in path {replica_folder_path}")
                    log_file.write(f"[{timestamp}] {file} was modified in path {replica_folder_path}\n\n")  

            files_names_replica_dup.remove(file)

    # Removing files from the Replica Folder that do not exist in the Source Folder.
    for file_erase in files_names_replica_dup:
        
        file_erase_path = os.path.join(replica_folder_path, file_erase)
        
        if os.path.exists(file_erase_path):
            
            # If it's a folder
            if os.path.isdir(file_erase_path):
                shutil.rmtree(file_erase_path)

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] {file_erase} and its content were removed from path {replica_folder_path}")
                log_file.write(f"[{timestamp}] {file_erase} and its content were removed from path {replica_folder_path}\n\n")  
            
            # If it's a file
            else:
                os.remove(file_erase_path)

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] {file_erase} was removed from path {replica_folder_path}")
                log_file.write(f"[{timestamp}] {file_erase} was removed from path {replica_folder_path}\n\n")  


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--source_folder", type=str, required=True, help="Source Folder Path" )
    parser.add_argument("--replica_folder", type=str, required=True, help="Replica Folder Path" )
    parser.add_argument("--sync_time", type=int, required=True, help="Synchronization time" )
    parser.add_argument("--log_file", type=str, required=True, help="Log File Path" )

    args = parser.parse_args()

    source_folder_path = args.source_folder
    replica_folder_path = args.replica_folder
    
    sync_time = int(args.sync_time)
    
    while(True):
        with open(args.log_file, "a") as log_file:
            sync_folders(source_folder_path, replica_folder_path, log_file)

        time.sleep(sync_time)


main()
