import re
import random
import string
import pandas as pd
from collections import defaultdict
from random_profile import RandomProfile


def random_char(char_num):
    """Random Character Generator"""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(char_num))


def random_email_gen(char_num=7):
    """Random Email Generator"""
    return random_char(char_num)+"@gmail.com"


def dms2dec(dms_str):
    """Return decimal representation of DMS"""
    """Reference: https://gist.github.com/chrisjsimpson/076a82b51e8540a117e8aa5e793d06ec"""
    dms_str = re.sub(r'\s', '', dms_str)
    sign = -1 if re.search('[swSW]', dms_str) else 1
    numbers = [*filter(len, re.split('\D+', dms_str, maxsplit=4))]
    degree = numbers[0]
    minute = numbers[1] if len(numbers) >= 2 else '0'
    second = numbers[2] if len(numbers) >= 3 else '0'
    frac_seconds = numbers[3] if len(numbers) >= 4 else '0'
    second += "." + frac_seconds
    return sign * (int(degree) + float(minute) / 60 + float(second) / 3600)


def create_customers(num_customers, driver=False):
    rp = RandomProfile()
    profiles = rp.full_profiles(num=num_customers)

    customers = defaultdict(list)
    for i, profile in enumerate(profiles):
        if driver:
            customers["DriverID"].append(i+1)
        else:
            customers["CustomerID"].append(i+1)
        customers["FirstName"].append(profile["first_name"])
        customers["LastName"].append(profile["last_name"])
        customers["Email"].append(profile["email"])
        customers["PhoneNumber"].append(profile["phone_number"])
        customers["Address"].append(
            ' '.join([str(val) for val in profile["address"].values()]))

        lat_dms = re.sub(r'\s', '', profile["coordinates"])[:16]
        lng_dms = re.sub(r'\s', '', profile["coordinates"])[16:]

        customers["HomeLat"].append(dms2dec(lat_dms))
        customers["HomeLong"].append(dms2dec(lng_dms))
    return pd.DataFrame.from_dict(customers)


def styled_print(text, header=False):
    """Custom Print Function"""
    class style:
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'

    if header:
        print(f'{style.BOLD}› {style.UNDERLINE}{text}{style.END}')
    else:
        print(f'    {text}')


def execute_and_commit(query, connection, cursor):
    """Execute and Commit SQL Query"""
    cursor.execute(query)
    connection.commit()


def fetch_data(query, cursor):
    """Fetch Data from Table by Executing SQL Query"""
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def insert_data(data_dict, table, cursor, connection):
    """Instert DataFrame data into Table"""
    styled_print(text=f"Populating {table}", header=True)
    # creating column list for insertion
    cols = "`,`".join([str(i) for i in data_dict.keys()])
    # Insert DataFrame recrds one by one.
    for i, row in data_dict.iterrows():
        sql = f"INSERT INTO `{table}` (`" + cols + \
            "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
        cursor.execute(sql, tuple(row))
        # the connection is not autocommitted by default, so we must commit to save our changes
        connection.commit()
