import random
import string
from randominfo import get_first_name, get_last_name, get_email


def random_char(char_num):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(char_num))


def random_email_gen(char_num=7):
    return random_char(char_num)+"@gmail.com"


def styled_print(text, header=False):
    class style:
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'

    if header:
        print(f'{style.BOLD}› {style.UNDERLINE}{text}{style.END}')
    else:
        print(f'    {text}')


def execute_and_commit(query, connection, cursor):
    cursor.execute(query)
    connection.commit()


def fetch_data(query, cursor):
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def insert_data(data_dict, table, cursor, connection):
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
