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
PARENT_PATH = './raw_file' # Must contain every csv file
QUERY_PATH = './query_folder' # Must contain every query
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

## Establish Connection with 6Sigma
host_name = "localhost"
user_name = "alexandre"
user_password = "Sigma64ever"
connection = create_server_connection(host_name, user_name, user_password)
db_name = 'base6sigma'
connection = create_db_connection(host_name, user_name, user_password, db_name)

## Get csv/scheme file for each table 
dir_ls = os.listdir(PARENT_PATH)   # list all csv file
dir_ls_query = os.listdir(QUERY_PATH)   # list all query file

for db_name in database_name :
    key = database_name[db_name]
    for file in dir_ls : 
        if key.lower().strip() in file.lower().strip() and ".csv" in file :
            database_file[db_name] = os.pathjoin(PARENT_PATH, 
			database_filename[db_name]=file
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
    
    schemepath = database_scheme[db_name]
    with open(schemepath,'r') as f:
        scheme = f.read() 
    print("#1 :")
    ex = execute_query(connection, f"DROP TABLE IF EXISTS`{db_name}_copy`")
    print("#2 :")
    ex = execute_query(connection, f"CREATE TABLE `{db_name}_copy` select * from `{db_name}`")
    print("#3 :")
    ex = execute_query(connection, f"DROP TABLE IF EXISTS `{db_name}`")
    print("#4 :")
    ex = execute_query(connection, scheme) # Create new table
    
    # 3/ Repopulate db
    populating_table_query(connection, df, db_name) # populate table
	filename = database_filename[db_name]
    move_to_folder(filename, PARENT_PATH, ARCHIVE_PATH) # move file into archive folder

input("Press Enter to continue...")