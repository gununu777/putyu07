# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, url_for, redirect
import MySQLdb
import datetime
app = Flask(__name__)
# ↑instance生成
# モデルは使わない。helloの中で全部やろう。→from models import db dbsql 
# これもつかわない→pip install flask-mysql
# これもつかわない→from flaskext.mysql import MySQL

###########################################
# routing functionを起動するURLを決める   #
###########################################
# "/"画面 index.htmlを表示する。3件の最新投稿を表示する画面。index.htmlにはinput画面へのhrefもある。

@app.route("/", methods=["GET", "POST"])
# toukouをviewするトップページ関数　mysqlからデータを取得しindex.htmlにkeyword argとしてresultを渡す resultにはmysqlから撮ってきたtoukouを渡す
def toukouview():
    if request.method != "GET":
        return render_template("input.html")
# mysqlへの接続＆cursorの定義
    connector = MySQLdb.connect(host="localhost", db="pytest", user="py", passwd="py", charset="utf8",)
#    connector = MySQLdb.connect(host="localhost", db="pytest", user="py", passwd="py", charset="utf8", cursorclass=MySQLdb.cursors.DictCursor )
    cursor = connector.cursor()
    # select sql pubdate降順に3件
    selectsql = "select * from keijiban order by pubdate DESC limit 3;"  
    cursor.execute(selectsql)
    result = cursor.fetchall()
    # たぶんクローズしないとダメそうな気がしていた
    connector.commit()
    cursor.close()
    connector.close()
    # レンダリングします
    return render_template("index.html", out=result)

# input画面
@app.route("/input", methods=["GET", "POST"])
# 投稿するメインの関数,id(32),text(140),投稿日時(date)をmysqlに渡すために存在する
def add_message():
# requestを取得して変数に格納する
    inputname = request.form['name'] 
    inputbody = request.form['body']
    # 指定の形式に時間帯文字列を作る
    d = datetime.datetime.today()
    pubdate = d.strftime("%Y/%m/%d %H:%M(%A)")
    # name length 計算
    namelength = len(inputname)
    if namelength >= 32:
        name = inputname[0:32]
    else:
        name = inputname
    # body length 計算
    bodylength = len(inputbody)
    if bodylength >= 140:
        body = inputbody[0:140]
    else:
        body = inputbody
    # 取得した3つの変数をmysqlに登録する
    insertsql = "insert into keijiban(name, body, pubdate) values('%s', '%s', '%s')" %(name, body, pubdate)
    connector = MySQLdb.connect(host="localhost", db="pytest", user="py", passwd="py", charset="utf8",)
#    connector = MySQLdb.connect(host="localhost", db="pytest", user="py", passwd="py", charset="utf8", cursorclass=MySQLdb.cursors.DictCursor )
    cursor = connector.cursor()
    cursor.execute(insertsql)
    # ホントはこのあとmysqlに書き込めたかどうかとか見たほうが良いのだろうと思うがそんな余裕はない。
    connector.commit()
    cursor.close()
    connector.close()
    # レンダリングします
    #return render_template('index.html')
    return redirect('/',)

# debugする設定にしておく    
if __name__ == "__main__":
    app.run(debug=True)

