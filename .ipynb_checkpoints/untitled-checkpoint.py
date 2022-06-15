import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
import os
import regex as re
import datetime 
import shutil
from tqdm import tqdm
from Kernel_lib import *

"""
This routine has been made to ease the importation of csv file into the 6Sigma Database
"""
## CONSTANT 
PARENT_PATH = './' # Must contain every csv file
QUERY_PATH = './' # Must contain every query
ARCHIVE_PATH = '/historique' # Folder for archive

#check_create_directory(ARCHIVE_PATH)    # Check if directory exist 
#check_create_directory(PARENT_PATH)    # Check if directory exist 

database_name = {"IT_Equipment": "IT_Equipment",
                 "Assets_new": "Assets",
                 "Olivier_it": "Olivier_it"
                }
database_file = {}
database_scheme = {}
database_filename = {}

## Get csv/scheme file for each table 
dir_ls = os.listdir(PARENT_PATH)   # list all csv file
dir_ls_query = os.listdir(QUERY_PATH)   # list all query file

for db_name in database_name :
    key = database_name[db_name]
    print(f"db name : {db_name} // keyword : {key}")
    for file in dir_ls : 
        if key.lower().strip() in file.lower().strip() and ".csv" in file :
            print(file)
            print('-'*5)
            database_file[db_name] = os.path.join(PARENT_PATH, file)
            database_filename[db_name] = file
            
    for file in dir_ls_query :
        
        if key.lower().strip() in file.lower().strip() and "sql_query" in file : 
            database_scheme[db_name] = os.path.join(QUERY_PATH, file)

for db_name in database_name :
    
    # 1/ get csv
    key = database_name[db_name]
    print(f"db name : {db_name} // keyword : {key}")
    filepath = database_file[db_name]
    df = get_csv_to_df(filepath)
    df = df.fillna("")
    
    # 2/ Make a copy + Drop
    print(f"name : {db_name} ")
    schemepath = database_scheme[db_name]
    with open(schemepath,'r') as f:
        scheme = f.read() 
    filename = database_filename[db_name]
    move_to_folder(filename, PARENT_PATH, ARCHIVE_PATH) # move file into archive folder
input("Press Enter to continue...")