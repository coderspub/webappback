import json

import pymysql
import pymongo
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/authorize', methods=['POST', 'GET'])
def authorize():
    if request.method == 'POST':
        b = request.get_json()
        u1 = b['user']
        p = b['password']
        print(b, u1, p)
    dba = pymysql.connect(host='localhost', user='root',password='Swathi_123', db='admin')
    mycursor = dba.cursor()
    mycursor.execute("SELECT * FROM customer_details WHERE customer_id=%s", [u1])
    result = mycursor.fetchone()
    print(result)
    if result:
        print("yes")
        if result[2] == p:
            val = json.dumps({'status': True, 'reason': 'successful'})
        else:
            val = json.dumps({'status': False, 'reason': 'Incorrect Password'})
    else:
        print("no")
        val = json.dumps({'status': False, 'reason': 'Incorrect Username'})
    dba.close()
    return val

@app.route('/location', methods=['POST', 'GET'])
def locate():
    if request.method == 'GET':
        customer_id = request.args.get('c_id')
        app_id = request.args.get('a_id')
        myclient=pymongo.MongoClient("mongodb://localhost:27017/")
        mydb=myclient[customer_id]
        mycol=mydb["tracking_details"]
        location=mycol.find_one({'app_id':app_id},{"_id":False})
        myclient.close()
        l=json.dumps(location)
    return l

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
