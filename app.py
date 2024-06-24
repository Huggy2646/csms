from flask import Flask, render_template, request, redirect,url_for,flash,make_response
import json
import datetime
import sys
import pymysql
import config


app = Flask(__name__)
db = config.db;

app.secret_key = "s_key"

# app.permanent_session_life=datetime.timedelta(minutes=10)

@app.route("/")
def index():
    # return "no"
    return "no"

@app.route("/market",methods=['GET','POST'])
def market():
    return "hello"
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        cursor=db.cursor()
        db.commit()
        id = request.form['id']
        pw = request.form['pw']

        cursor.execute('SELECT * FROM Id_Pw WHERE std_num = %s AND std_pw = %s', (id, pw))
        result = cursor.fetchone()
        if result:
            cursor.close()
            return "yes"
        else:
            return "no"
    return "no"

# @app.route("/re",methods=['GET','POST'])
# def re():
#     print("re")
#     cusrsor=db.cursor()
#     db.commit()
#     class_num = request.args.get['class_num'];
#     query='SELECT seat_num,std_num FROM {} where std_num IS NOT null'.format(class_num)
#     cursor.execute(query)
#     data=json.dumps(cursor.fetchall())
#     if data:
#         cursor.close()
#         return redirect(url_for('/class_n'),asd=data)
    
# 앉은자리 좌표 읽어오기
@app.route("/class_n",methods=['GET','POST'])
def class_n():
    # with
    cursor=db.cursor()
    db.commit()
    # if request.method=='get':
    #     print(request.args.get('asd'))
    #     return request.args.get('asd')
    if request.method=='POST':
        # config.db.commit() #데베 새로고침
        # print(request.form['class_num'])
        class_num = request.form['class_num'];
        query='SELECT seat_num,std_num FROM {} where std_num IS NOT null'.format(class_num)

        cursor.execute(query)

        data=json.dumps(cursor.fetchall())
        # print(type(data))
        print(data)
        
        if data:
            cursor.close()
            print("okhttp")
            return data
        else:
            return 'no'
        return "yes"
    return "no"

#update seat_num
@app.route("/update",methods=['POST','GET'])
def update():
    cursor=db.cursor()
    db.commit()
    if request.method=='POST':
        if request.form['seat_num']:
            c_n = request.form['class_num']
            id = request.form['id']
            s_n = request.form['seat_num']
            #자기 자리 유무
            # query = 'select seat_num from {} where std_num={};'.format(request.form['seat_num'],request.form['class_num'],request.form['id'])
            query_0 = 'select seat_num from {} where std_num={};'.format(c_n,id)
            query ='SELECT std_num FROM {} where seat_num="{}";'.format(c_n,s_n)
            
            #자리 유무
            cursor.execute(query_0)
            myseat = cursor.fetchone()
            cursor.execute(query)
            seat_is_full = cursor.fetchone()
            
            if myseat:
                query_1 = 'update {} set std_num=NULL where seat_num="{}";'.format(c_n,myseat[0])
                query_2 = 'update {} set std_num={} where seat_num="{}";'.format(c_n,id,s_n)
                cursor.execute(query_1)
                cursor.execute(query_2)
                db.commit()
            # result = cursor.fetchone()
            # if result:
                
            #새로운 자리 선정
            # print(request.form['seat_num'])
            # print(request.form['id'])
            # print(request.form['class_num'])
            else:
                query = 'update {} set std_num={} where seat_num="{}";'.format(c_n,id,s_n)
                print(query)
            cursor.execute(query)
            db.commit()
            cursor.close()
        return "yes" #redirect(url_for('re',class_num=c_n))
    return redirect(url_for('re',class_num=c_n))
            # flash('update')
    
@app.route("/delete",methods=['GET','POST'])
def delete():
    cursor=db.cursor()
    print(request.form['id'])
    print(request.form['class_num'])
    if  request.method=='POST':
        if request.form['id']:
            query = 'update {} set std_num=null where std_num={}'.format(request.form['class_num'],
                                                                         request.form['id']
                                                                        )
            cursor.execute(query)
            db.commit()
            cursor.close()
            return 'yes'
        return 'no'
    return 'no'
# @app.route("/logout",methods=['GET','POST'])
# def logout():
#     Session.clear()
#     return 'yes'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    # app.endpoint()