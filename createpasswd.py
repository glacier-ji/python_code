#!/usr/bin/python env

import string
import random



def get_pw():
    pw = []
    for i in range(5):
        pw.append(random.choice(string.lowercase))
        pw.append(random.choice(string.uppercase))
        pw.append(random.choice(string.digits))
    random.shuffle(pw)
    pw = ''.join(pw)
    return pw


if __name__ == '__main__':
    #get_pw()
    infile = open('svnpassword.txt', 'w')
    with open('user.txt', 'rw') as f:
        for username in f:
            infile.write(username.strip() + '=' + get_pw() + '\n')
    infile.close 
