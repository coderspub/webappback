import json

import pymysql.cursors
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/authorize',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      password = request.form['ps']
      #print user,password
      return 'ok'

@app.route('/authorize/<user>/<password>')
def authorize(user,password):
   p=str(password)
   u1=str(user)
   dba = connection = pymysql.connect(host='localhost',user='root', password='Swathi_123',db='admin')
   mycursor = dba.cursor()

   values = mycursor.execute("SELECT customer_id FROM customer_details")
   result =list(mycursor.fetchall())
   l= len(result)
   user_list=[]
   for i in range (l):
      u2=str((result[i])[0])
      user_list.append(u2)
   if u1 in user_list:
      values1 = mycursor.execute("SELECT password FROM customer_details WHERE customer_id=%s",[u1])
      result1 =mycursor.fetchone()
      r=result1[0]
      if r==p:
         val=json.dumps({'status':True})
      else:
         val=json.dumps({'status':False})
   else:
      val=json.dumps({'status':False})
   dba.close()
   return val


@app.route('/location',methods = ['POST', 'GET'])
def locate():
   if request.method == 'GET':
      customer_id = request.args.get('c_id')
      app_id = request.args.get('a_id')
      dba = connection = pymysql.connect(host='localhost',user='root', password='Swathi_123',db=customer_id)
      mycursor = dba.cursor()
      values = mycursor.execute("SELECT latitude, longitude FROM tracking_details WHERE app_id=%s ORDER BY id DESC LIMIT 1",[app_id])
      result =mycursor.fetchall()
      l1={'latitude':(result[0])[0],'longitude':(result[0])[1]}
      l2=json.dumps(l1)
      dba.close()
   return l2

#to send json data
"""@app.route('/loca/')
def lo():
    k={'tyt':'swa','lus':'sha'}
    l=json.dumps(k)
    return l"""
      

if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True)
