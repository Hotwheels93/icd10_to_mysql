# Author: Martin Hocquel
# Date: 2023-04-20
# Description: This script reads the ICD-10-GM file and inserts the ICD-10 codes into a MySQL database.
# Copyrigth: (c) Martin Hocquel 2023
# Website: https://www.0verflow.de
# GitHub Repo: https://github.com/Hotwheels93/icd10_to_mysql
# Licence: MIT
# Version: 0.1 (2023-04-20)

import ast
import mysql.connector
import sys
import time

icd10_filepath = "icd10gm2023syst_kodes_20221206.txt" # change this to the path of your ICD-10 file

def file_to_dict(file_path):
    global icd_dict
    icd_dict = dict()
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            line = line.split(";") # Split the line into a list
            icd_dict[line[6]] = line[8] # line[6] = ICD-10 code, line[8] = diagnose text

def create_dict():
    file_to_dict(icd10_filepath)
    with open('icd10gm.txt', 'w') as f:
        print(icd_dict, file=f)


def progress_bar(current, total, start_time, bar_length=40):
    elapsed_time = time.time() - start_time
    percent = float(current) * 100 / total
    arrow = '-' * int(percent / 100 * bar_length - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    eta = (elapsed_time * (total / current)) - elapsed_time
    sys.stdout.write('\rProgress: [%s%s] %d%% | Elapsed Time: %ds | ETA: %ds | Inserted: %d of %d' % (arrow, spaces, percent, elapsed_time, eta, current, total))
    sys.stdout.flush()

def count_icd10_codes(file_path):
    with open(file_path, "r") as f:
        icd_dict_str = f.read()
        icd_dict = ast.literal_eval(icd_dict_str)
    return len(icd_dict)

def insert_icd10_codes_to_database(icd_dict, db_config):
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    insert_query = """
        INSERT INTO icd10_keys (icd10_code, icd10_alternative_code, diagnose_text)
        VALUES (%s, %s, %s);
    """

    total = len(icd_dict)
    count = 0
    start_time = time.time()

    for icd_code, diagnose_text in icd_dict.items():
        icd10_alternative_code = "" # empty string for alternative icd10 code
        data = (icd_code, icd10_alternative_code, diagnose_text)

        try:
            cursor.execute(insert_query, data)
            count += 1
            progress_bar(count, total, start_time)
        except mysql.connector.Error as err:
            print(f"\nError inserting data for ICD-10 code {icd_code}: {err}")
            continue

    cnx.commit()
    cursor.close()
    cnx.close()

    print(f"\n\nInsert process completed. {count} out of {total} datasets were inserted successfully.")

if __name__ == "__main__":

    print("Converting ICD10-GM file...")
    create_dict() # read and convert the ICD-10 file to a dictionary

    file_path = "icd10gm.txt"
    
    count = count_icd10_codes(file_path)
    print(f"There are {count} ICD-10 codes in the file '{file_path}'.")

    with open(file_path, "r") as f:
        icd_dict_str = f.read()
        icd_dict = ast.literal_eval(icd_dict_str)

    # Database connection configuration, CHANGE THIS TO YOUR OWN CONFIGURATION
    db_config = {
        "host": "YOUR_MYSQL_HOST",
        "user": "YOUR_DB_USER",
        "password": "YOUR_DB_PW",
        "database": "YOUR_DB_NAME"
    }

    insert_icd10_codes_to_database(icd_dict, db_config)
