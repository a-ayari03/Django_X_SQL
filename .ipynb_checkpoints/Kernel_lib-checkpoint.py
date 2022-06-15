import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
import os
import regex as re
import datetime 
import shutil
from tqdm import tqdm

## DB Connection 
def create_server_connection(host_name, user_name, user_password):
    '''
    Establish a server connection using creditential
    Parameters
    ----------
    host_name : str
        host_name
    user_name : str
        user_name
    user_password : str
        user_password
    
    Returns
    -------
    connection : obj
        server connection object
    '''
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_db_connection(host_name, user_name, user_password, db_name):
    '''
    Establish a database connection using creditential and db_name name
    Parameters
    ----------
    host_name : str
        host name
    user_name : str
        user name
    user_password : str
        user password
    db_name : str
        database name
    
    Returns
    -------
    connection : obj
        server connection object
    '''
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database = db_name
            
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    '''
    Function to execute query, should be used with CREATE, ALTER, UPDATE, ..
    Parameters
    ----------
    connection : obj
        server connection object
    query : str
        SQL query
    
    Returns
    -------
    connection : obj
        server connection object
    '''
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit() # implement our query 
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
        
def read_query(connection, query):
        '''
    function to read SQL query, should be used with SELECT, .. 
    Parameters
    ----------
    connection : obj
        server connection object
    query : str
        SQL query
    
    Returns
    -------
    connection : obj
        server connection object
    '''
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error: '{err}'")

def populating_table_query(connection, df, file) :
    """
    SQL query for inserting rows into a table based on a Dataframe
    """
    LOG_EVERY_N = 2000
    for i, row in tqdm(df.iterrows(), total = df.shape[0], desc=f"uploading file {str(file)} ..") :
        query = f"INSERT `{file}` VALUES ("+ "%s,"*(len(row)-1)+ "%s)"
        
        cursor = connection.cursor()
        try:

            cursor.execute(query, tuple(row))
            connection.commit() # implement our query 
            if (i % LOG_EVERY_N) == 0 :
                print(f"Record inserted n°{i}")
        except Error as err:
            if (i % LOG_EVERY_N) == 0 :
                print(f"Error: '{err}'")

## CSV engineering 

def get_csv_to_df(filepath : str, filename = None , datetime = None) :
    try :
        
        df = pd.read_csv(filepath, header = None, delimiter = ',', encoding='latin-1') 
        if filename != None or datetime != None : 
            df["SOURCES"] = filename
            df['timestamp'] = datetime.strftime('%d-%m-%y')
        if "asset_id" in str(df.iloc[0].str.lower().values).lower().strip() :    # if csv have header
            df = pd.read_csv(filepath, header = 0, delimiter = ',', encoding='latin-1') 
            if filename != None or datetime != None : 
                df["SOURCES"] = filename
                df['timestamp'] = datetime.strftime('%d-%m-%y')
        
    except pd.errors.ParserError:
        df = pd.read_csv(filepath, header = None, delimiter = ';', encoding='latin-1') 
        if filename != None or datetime != None : 
            df["SOURCES"] = filename
            df['timestamp'] = datetime.strftime('%d-%m-%y')
        if "asset_id" in str(df.iloc[0].str.lower().values).lower().strip() :    # if csv have header
            df = pd.read_csv(filepath, header = 0, delimiter = ';', encoding='latin-1') 
            if filename != None or datetime != None : 
                df["SOURCES"] = filename
                df['timestamp'] = datetime.strftime('%d-%m-%y')
    
    return df

## File / Os def

def check_create_directory(path: str) :
    """
    Check if path exist, if not create every intermediate folder
    """

    if os.path.exists(path) == False :
        os.makedirs(path)
    return True

def move_to_folder(file: str, current_folder: str, new_folder: str) :
    
    """
    Move a file to a specified folder
    """
	
    current_file = os.path.join(current_folder, file)
    new_file = os.path.join(new_folder, file)
	
	print("current_file", current_file)
	print("new_file", new_file)
    shutil.move(current_file, new_file)
    
    return True