import sys
import hashlib
import getpass
import sqlite3



def get_info():
    info = []
    user_name = raw_input('Please Enter a User Name: ')
    password = hashlib.sha224(getpass.getpass('Please Enter a Password: ')).hexdigest()
    info.append((user_name, password))
    return info


def main():
        info = get_info()
        try:
            conn = sqlite3.connect('pub.db')
            cu = conn.cursor()
            sql = '''
                 insert into USER values (?,?)
                 '''
            cu.execute(sql, info[0])
            conn.commit()
        except:
                sys.exit('error!')


if __name__ == "__main__":
        main()
