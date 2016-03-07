import sys
import hashlib
import getpass
import sqlite3

def main():
    user_name = raw_input('Please Enter User Name: ')
    user_pass = hashlib.sha224(getpass.getpass('Please Enter Password: ')).hexdigest()
    conn = sqlite3.connect('pub.db')
    cu = conn.cursor()
    sql = '''
          select name,pass from user where name = ?
          '''
    cu.execute(sql, (user_name,))
    uname,pw = cu.fetchone()

    pass_try = 0 
    x = 3
 
    while pass_try < x:
        if user_pass != pw:
             print 'Incorrect Password, ' + str(x-pass_try) + ' more attemts left\n'
             user_pass = hashlib.sha224(getpass.getpass('Please Enter Password: ')).hexdigest()
             pass_try += 1
        else:
            print 'User is logged in!\n'
            sys.exit()

if __name__ == "__main__":
    main()
