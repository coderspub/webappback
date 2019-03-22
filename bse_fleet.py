from flask import Flask, render_template, request
app = Flask(__name__)
import MySQLdb

""""@app.route('/authori',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      password = request.form['ps']
      print user,password
   return 'ok'"""

@app.route('/authorize/<user>/<passw>')
def authorize(user,passw):
   p=str(passw)
   u1=str(user)
   dba = MySQLdb.connect(host="localhost", user="root", passwd="Swathi_123", db="admin")
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
	    val='authorized user'
          else:
	    val='unauthorized user'
   else:
	 val='unauthorized user'


   
   dba.close()
   return val

if __name__ == '__main__':
   app.run(debug = True)
