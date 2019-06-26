#!/home/suriya/virtual_env_python/fleet_1/bin/python
import random
from datetime import datetime
from email.mime.text import MIMEText as t2b
from smtplib import SMTP
import logging
from logging.handlers import RotatingFileHandler
import base64

import pymongo
import pymysql
from flask import Flask, jsonify, render_template, request, json
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt

log_file='/home/suriya/webappback.log'

app = Flask(__name__)
CORS(app)
handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
app.logger.addHandler(handler)
bcrypt=Bcrypt()

def database(db1='fleet_admin'):
    return pymysql.connect(host='localhost', user='fleet',password='Fleet@123', db=db1, cursorclass=pymysql.cursors.DictCursor)

@app.errorhandler(Exception)
def exceptions(e):
    """ Logging after every Exception. """
    app.logger.error('%s %s %s 5xx INTERNAL SERVER ERROR\n%s',request.remote_addr,request.method,request.full_path,e)
    return "Internal Server Error",500

@app.errorhandler(404)
def notfound(e):
    return "The endpoint not found. Please check the endpoint and try again",404

@app.route('/log')
def log():
    with open(log_file, 'r+') as f:
        content = f.read()
    c =content.split("\n")
    return render_template('log.html',len = len(c) ,text=c)

@app.route('/Authorize', methods=['POST'])
def Authorize():
    if request.method == 'POST':
        data = request.get_json()
        dba = database()
        with dba.cursor() as cur:
            cur.execute("SELECT passwd FROM reg_user WHERE email_id=%s",(data['email_id']))
            result = cur.fetchone()
        dba.close()
        if result:
            if bcrypt.check_password_hash(result['passwd'],data['passwd']):
                return jsonify({'status': True, 'reason': 'successful'})
            else:
                return jsonify({'status': False, 'reason': 'Incorrect Password'})
        else:
            return jsonify({'status': False, 'reason': 'Incorrect Username'})

@app.route('/Location', methods=['POST'])
def Location():
    if request.method == 'POST':
        data = request.get_json()
        dba = database()
        with dba.cursor() as cur:
            cur.execute("SELECT db FROM reg_user WHERE email_id=%s",(data['email_id']))
            result = cur.fetchone()
        dba.close()
        if result!=None:
            dba = database(result['db'])
            with dba.cursor() as cur:
                cur.execute("SELECT ST_AsGeoJson(location) as location, DATE_FORMAT(datetime,'%%Y-%%m-%%d %%H:%%i:%%s') as datetime, speed FROM app_tracking_details WHERE appid=%s ORDER BY id DESC LIMIT 1",(data['appid']))
                result = cur.fetchone()
            dba.close()
            if result:
                result['location']=json.loads(result['location'])
                return jsonify({'status':True,'reason':'successful','trackingdetail':result})
            else:
                return jsonify({'status':False,'reason':'appid not exist'})
        else:
            return jsonify({'status':False,'reason':'Wrong email'})

@app.route('/SignUpOTP',methods=['POST'])
def SignUpOTP():
    if request.method=='POST':
        data=request.get_json()
        dba = database()
        with dba.cursor() as cur:
            cur.execute("SELECT email_id FROM reg_user WHERE email_id=%s",(data['email_id']))
            result = cur.fetchone()
            if result==None:
                otp_value=random.randrange(0,999999)
                s_email='xcompassfms@gmail.com'
                passwd='fma!@345'
                message='This is the OTP to Signup : %s'%otp_value
                msg=t2b(message)
                msg['Subject']='Signup OTP'
                msg['From']=s_email
                msg['To']=data['email_id']
                ser=SMTP('smtp.gmail.com',587)
                ser.starttls()
                ser.login(s_email,passwd)
                ser.send_message(msg)
                ser.quit()
                cur.execute("INSERT INTO temp_signup (email_id, otp,verify) VALUES (%s,%s,0)",(data['email_id'],otp_value))
                dba.commit()
                dba.close()
                return jsonify({'status': True, 'reason': 'Not exist and otp send'})
            else:
                dba.close()
                return jsonify({'status': False, 'reason': 'already exist'})

@app.route('/VerifyOTP',methods=['POST'])
def VerifyOTP():
    if request.method=='POST':
        data=request.get_json()
        dba = database()
        with dba.cursor() as cur:
            cur.execute("SELECT otp FROM temp_signup WHERE email_id=%s",(data['email_id']))
            result = cur.fetchone()
            if result:
                if result['otp']==int(data['otp']):
                    cur.execute("UPDATE temp_signup SET verify=1 WHERE email_id=%s",(data['email_id']))
                    dba.commit()
                    dba.close()
                    return jsonify({'status':True,'reason':'successful'})
                else:
                    dba.close()
                    return jsonify({'status':False,'reason':'Wrong OTP'})
            else:
                dba.close()
                return jsonify({'status':False,'reason':'Wrong email'})

@app.route('/SignUp',methods=['POST'])
def SignUp():
    if request.method=='POST':
        data=request.get_json()
        data['passwd']=bcrypt.generate_password_hash(data['passwd'])
        dba = database()
        with dba.cursor() as cur:
            cur.execute("SELECT verify FROM temp_signup WHERE email_id=%s",(data['email_id']))
            result = cur.fetchone()
            if result:
                if result['verify']==1:
                    db_name='fms_'+base64.b64encode(data['email_id'])
                    cur.execute("INSERT INTO reg_user (email_id,passwd,db,company_name,phonenumber,address,country,zipcode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(data['email_id'],data['passwd'],db_name,data['company_name'],data['phonenumber'],data['address'],data['country'],data['zipcode']))
                    cur.execute("DELETE FROM temp_signup WHERE email_id=%s",(data['email_id']))
                    cur.execute("CREATE DATABASE %s"%db_name)
                    dba.commit()
                    dba.close()
                    dba = database(db_name)
                    with dba.cursor() as cur:
                        cur.execute("CREATE TABLE applist (id INT PRIMARY KEY AUTO_INCREMENT,employee_name VARCHAR(20),phonenumber VARCHAR(20),designation VARCHAR(20),appid VARCHAR(20),datetime DATETIME DEFAULT CURRENT_TIMESTAMP)")
                        cur.execute("CREATE TABLE app_tracking_details (id INT PRIMARY KEY AUTO_INCREMENT,location POINT,speed VARCHAR(20),accuracy VARCHAR(50),datetime DATETIME DEFAULT CURRENT_TIMESTAMP,appid VARCHAR(20))")
                        dba.commit()
                    dba.close()
                    return jsonify({'status':True,'reason':'successful'})
                else:
                    dba.close()
                    return jsonify({'status':False,'reason':'otp not verified'})
            else:
                dba.close()
                return jsonify({'status':False,'reason':'otp expired'})

@app.route('/AppReg', methods=['POST'])
def AppReg():
    if request.method == 'POST':
        data = request.get_json()
        dba = database()
        with dba.cursor() as cur:
            cur.execute("SELECT db FROM reg_user WHERE email_id=%s",(data['email_id']))
            result = cur.fetchone()
        dba.close()
        if result!=None:
            dba = database(result['db'])
            with dba.cursor() as cur:
                cur.execute("SELECT appid FROM applist ORDER BY id DESC LIMIT 1")
                result = cur.fetchone()
                if result!=None:
                    appid='app'+str(int(result['appid'][3:])+1)
                else:
                    appid="app1"
                cur.execute("INSERT INTO applist (employee_name,phonenumber,designation,appid) VALUES (%s,%s,%s,%s)",(data['employee_name'],data['phonenumber'],data['designation'],appid))
                dba.commit()
            dba.close()
            return jsonify({'status':True,'reason':'successful'})
        else:
            return jsonify({'status':False,'reason':'Wrong email'})

@app.route('/AppList', methods=['POST'])
def AppList():
    if request.method == 'POST':
        data = request.get_json()
        dba = database()
        with dba.cursor() as cur:
            cur.execute("SELECT db FROM reg_user WHERE email_id=%s",(data['email_id']))
            result = cur.fetchone()
        dba.close()
        if result!=None:
            dba = database(result['db'])
            with dba.cursor() as cur:
                cur.execute("SELECT employee_name,phonenumber,designation,appid FROM applist")
                result = cur.fetchall()
            dba.close()
            return jsonify({'status':True,'reason':'successful','applist':result})
        else:
            return jsonify({'status':False,'reason':'Wrong email'})

@app.route('/AppDetail', methods=['POST'])
def AppDetail():
    if request.method == 'POST':
        data = request.get_json()
        dba = database()
        with dba.cursor() as cur:
            cur.execute("SELECT db FROM reg_user WHERE email_id=%s",(data['email_id']))
            result = cur.fetchone()
        dba.close()
        if result!=None:
            dba = database(result['db'])
            with dba.cursor() as cur:
                cur.execute("SELECT employee_name,phonenumber,designation,appid FROM applist WHERE appid=%s",(data['appid']))
                result = cur.fetchone()
            dba.close()
            if result:
                return jsonify({'status':True,'reason':'successful','appdetail':result})
            else:
                return jsonify({'status':False,'reason':'appid not exist'})
        else:
            return jsonify({'status':False,'reason':'Wrong email'})

@app.route('/AppEdit', methods=['POST'])
def AppEdit():
    if request.method == 'POST':
        data = request.get_json()
        dba = database()
        with dba.cursor() as cur:
            cur.execute("SELECT db FROM reg_user WHERE email_id=%s",(data['email_id']))
            result = cur.fetchone()
        dba.close()
        if result!=None:
            dba = database(result['db'])
            with dba.cursor() as cur:
                cur.execute("SELECT appid FROM applist WHERE appid=%s",(data['appid']))
                result = cur.fetchone()
                if result!=None:
                    cur.execute("UPDATE applist SET employee_name=%s,phonenumber=%s,designation=%s WHERE appid=%s",(data['employee_name'],data['phonenumber'],data['designation'],data['appid']))
                    dba.commit()
                    dba.close()
                    return jsonify({'status':True,'reason':'successful'})
                else:
                    dba.close()
                    return jsonify({'status':False,'reason':'appid not exist'})
        else:
            return jsonify({'status':False,'reason':'Wrong email'})

@app.route('/AppRemove', methods=['POST'])
def AppRemove():
    if request.method == 'POST':
        data = request.get_json()
        dba = database()
        with dba.cursor() as cur:
            cur.execute("SELECT db FROM reg_user WHERE email_id=%s",(data['email_id']))
            result = cur.fetchone()
        dba.close()
        if result!=None:
            dba = database(result['db'])
            with dba.cursor() as cur:
                cur.execute("SELECT appid FROM applist WHERE appid=%s",(data['appid']))
                result = cur.fetchone()
                if result!=None:
                    cur.execute("DELETE FROM applist WHERE appid=%s",(data['appid']))
                    dba.commit()
                    dba.close()
                    return jsonify({'status':True,'reason':'successful'})
                else:
                    dba.close()
                    return jsonify({'status':False,'reason':'appid not exist'})
        else:
            return jsonify({'status':False,'reason':'Wrong email'})

@app.route('/UserDetail', methods=['POST'])
def UserDetail():
    if request.method == 'POST':
        data = request.get_json()
        dba = database()
        with dba.cursor() as cur:
            cur.execute("SELECT email_id,company_name,phonenumber,address,country,zipcode FROM reg_user WHERE email_id=%s",(data['email_id']))
            result = cur.fetchone()
        dba.close()
        if result!=None:
            return jsonify({'status':True,'reason':'successful','userdetail':result})
        else:
            return jsonify({'status':False,'reason':'Wrong email'})

@app.after_request
def after_request(response):
    """ Logging after every request. """
    if response.status_code != 500:
        app.logger.error('%s %s %s %s'%(request.remote_addr,request.method,request.full_path,response.status))
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
