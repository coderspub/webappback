import json
import random
from datetime import datetime
import pymysql
import pymongo
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from smtplib import SMTP
from email.mime.text import MIMEText as t2b

app = Flask(__name__)
CORS(app)

@app.route('/Authorize', methods=['POST', 'GET'])
def Authorize():
    if request.method == 'POST':
        data = request.get_json()
        u1 = data['email_id']
        p = data['passwd']
    dba = pymysql.connect(host='localhost', user='fleet',password='Fleet@123', db='fleet_admin')
    mycursor = dba.cursor()
    mycursor.execute("SELECT passwd FROM reg_user WHERE email_id=%s",[u1])
    result = mycursor.fetchone()
    if result:
        if result[0] == p:
            d = {'status': True, 'reason': 'successful'}
        else:
            d = {'status': False, 'reason': 'Incorrect Password'}
    else:
        d = {'status': False, 'reason': 'Incorrect Username'}
    dba.close()
    d=json.dumps(d)
    return d

@app.route('/Location', methods=['POST', 'GET'])
def Location():
    if request.method == 'POST':
        data=request.get_json()
        print(data)
        customer_id = data['c_id']
        app_id = data['a_id']
        myclient=pymongo.MongoClient("mongodb://localhost:27017/")
        mydb=myclient[customer_id]
        mycol=mydb["tracking_details"]
        location=mycol.find_one({'app_id':app_id},{"_id":False})
        myclient.close()
        d=json.dumps(location)
        print(d)
    return d

@app.route('/Devices', methods=['POST', 'GET'])
def Devices():
    if request.method == 'POST':
        data = request.get_json()
        customer_id = data['c_id']
        dba = pymysql.connect(host='localhost', user='fleet',password='Fleet@123', db='fleet_admin')
        mycursor = dba.cursor()
        mycursor.execute("SELECT app_id FROM app_details WHERE customer_id=%s", [customer_id])
        result = mycursor.fetchall()
        devs=[]
        for i in result:
            devs.append(i[0])
        d={"devices":devs,"nod":len(result)}    
        d=json.dumps(d)
        dba.close()
    return d

@app.route('/SignUpOTP',methods=['POST','GET'])
def SignUpOTP():
    if request.method=='POST':
        data=request.get_json()
        email_id=data['email_id']
        dba = pymysql.connect(host='localhost', user='fleet',password='Fleet@123', db='fleet_admin')
        mycursor = dba.cursor()
        mycursor.execute("SELECT email_id FROM reg_user WHERE email_id=%s",[email_id])
        result = mycursor.fetchone()
        if result==None:
            d={'status': True, 'reason': 'Not exist and otp send'}
            otp_value=random.randrange(0,999999)
            s_email='xcompassfms@gmail.com'
            passwd='fma!@345'
            message='This is the OTP to Signup : %s'%otp_value
            msg=t2b(message)
            msg['Subject']='Signup OTP'
            msg['From']=s_email
            msg['To']=email_id
            ser=SMTP('smtp.gmail.com',587)
            ser.starttls()
            ser.login(s_email,passwd)
            ser.send_message(msg)
            ser.quit()
            dt=str(datetime.now())
            mycursor.execute("INSERT INTO temp_signup (email_id, otp,datetime,verify) VALUES (%s,%s,%s,0)",(email_id,otp_value,dt))
            dba.commit()
        else:
            d={'status': False, 'reason': 'already exist'}
        dba.close()
        d=json.dumps(d)
        return d

@app.route('/VerifyOTP',methods=['POST','GET'])
def VerifyOTP():
    if request.method=='POST':
        data=request.get_json()
        email_id=data['email_id']
        otp_value=data['otp']
        dba = pymysql.connect(host='localhost', user='fleet',password='Fleet@123', db='fleet_admin')
        mycursor = dba.cursor()
        mycursor.execute("SELECT otp FROM temp_signup WHERE email_id=%s",[email_id])
        result = mycursor.fetchone()
        if result:
            if result[0]==int(otp_value):
                d={'status':True,'reason':'successful'}
                mycursor.execute("UPDATE temp_signup SET verify=1 WHERE email_id=%s",[email_id])
                dba.commit()
            else:
                d={'status':False,'reason':'Wrong OTP'}
        else:
            d={'status':False,'reason':'Wrong email'}
        dba.close()
        d=json.dumps(d)
        return d

@app.route('/SignUp',methods=['POST','GET'])
def SignUp():
    if request.method=='POST':
        data=request.get_json()
        email_id=data['email_id']
        dba = pymysql.connect(host='localhost', user='fleet',password='Fleet@123', db='fleet_admin')
        mycursor = dba.cursor()
        mycursor.execute("SELECT verify FROM temp_signup WHERE email_id=%s",[email_id])
        result = mycursor.fetchone()
        if result:
            if result[0]==1:
                d={'status':True,'reason':'successful'}
                mycursor.execute("SELECT db FROM reg_user ORDER BY id DESC LIMIT 1")
                result=mycursor.fetchone()
                db_name='fma'+str(int(result[0][3:])+1)
                address=data['address']
                company_name=data['company_name']
                passwd=data['passwd']
                country=data['country']
                phonenumber=data['phonenumber']
                zipcode=data['zipcode']
                dt=str(datetime.now())
                mycursor.execute("INSERT INTO reg_user (email_id,passwd,db,company_name,phonenumber,address,country,zipcode,datetime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(email_id,passwd,db_name,company_name,phonenumber,address,country,zipcode,dt))
                dba.commit()
                mycursor.execute("DELETE FROM temp_signup WHERE email_id=%s",[email_id])
                dba.commit()
                mycursor.execute("CREATE DATABASE %s",[db_name])
                dba.commit()
            else:
                d={'status':False,'reason':'otp not verified'}
        else:
            d={'status':False,'reason':'otp expired'}
        d=json.dumps(d)
        return d

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)