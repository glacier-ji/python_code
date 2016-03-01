#coding=utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, g,url_for,request,render_template 

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'sndb'),
    DEBUG=True
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect("/home/query_sn/sndb")
    rv.text_factory = str
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/',methods=['GET', 'POST'])
def calmo():
    total = None
    sn = []
    db = get_db()
    sum_list = []
    query = """select * from zc where sn = ?"""
    if request.method == 'POST':
        data = request.form['sn']
        sn = data.split()
        for s in sn:
            cur = db.execute(query, (s,))
            for sn,money,project,pro_id in cur.fetchall():
                sum_list.append(money)
        total = sum(sum_list)
    return render_template('cal.html', total=total)

@app.route('/show',methods=['GET', 'POST'])
def show_pro():
    all_pro = None
    db = get_db()
    query = """select project, SUM(money) from zichan group by project"""
    cur = db.execute(query)
    allpro = cur.fetchall()[1:]
    return render_template('show_pro.html', allpro=allpro)

if __name__ == '__main__':
    app.run()

