from flask import Flask, render_template, flash, request, session,send_file
from flask import render_template, redirect, url_for, request


import sys

import pickle
import numpy as np




import ibm_db
import pandas
import ibm_db_dbi
from sqlalchemy import create_engine


engine = create_engine('sqlite://',
                       echo = False)

dsn_hostname = "125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
dsn_uid = "jft01867"
dsn_pwd = "UkVOMQdSAOdR9NmF"

dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "BLUDB"
dsn_port = "30426"
dsn_protocol = "TCPIP"
dsn_security = "SSL"

dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd,dsn_security)



try:
    conn = ibm_db.connect(dsn, "", "")
    print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)

except:
    print ("Unable to connect: ", ibm_db.conn_errormsg() )



app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.route("/")
def homepage():

    return render_template('index.html')

@app.route("/AdminLogin")
def AdminLogin():

    return render_template('AdminLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')

@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')

@app.route("/NewQuery1")
def NewQuery1():
    return render_template('NewQueryReg.html')





@app.route("/AdminHome")
def AdminHome():
    conn = ibm_db.connect(dsn, "", "")
    pd_conn = ibm_db_dbi.Connection(conn)

    selectQuery = "SELECT * from regtb "
    dataframe = pandas.read_sql(selectQuery, pd_conn)

    dataframe.to_sql('Employee_Data',
                     con=engine,
                     if_exists='append')

    # run a sql query
    data = engine.execute("SELECT * FROM Employee_Data").fetchall()
    return render_template('AdminHome.html',data=data)






@app.route("/UserHome")
def UserHome():
    user = session['uname']

    conn = ibm_db.connect(dsn, "", "")
    pd_conn = ibm_db_dbi.Connection(conn)
    selectQuery = "SELECT * FROM regtb where  UserName= '" + user + "' "
    dataframe = pandas.read_sql(selectQuery, pd_conn)
    dataframe.to_sql('booktb1', con=engine, if_exists='append')
    data = engine.execute("SELECT * FROM booktb1").fetchall()
    return render_template('UserHome.html',data=data)


@app.route("/UQueryandAns")
def UQueryandAns():


    uname = session['uname']

    conn = ibm_db.connect(dsn, "", "")
    pd_conn = ibm_db_dbi.Connection(conn)
    selectQuery = "SELECT * FROM querytb  where  UserName= '" + uname + "' "
    dataframe = pandas.read_sql(selectQuery, pd_conn)
    dataframe.to_sql('booktb1', con=engine, if_exists='append')
    data = engine.execute("SELECT * FROM booktb1").fetchall()


    return render_template('UserQueryAnswerinfo.html', data=data )


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
       if request.form['uname'] == 'admin' or request.form['password'] == 'admin':

           conn = ibm_db.connect(dsn, "", "")
           pd_conn = ibm_db_dbi.Connection(conn)
           selectQuery = "SELECT * FROM regtb  "
           dataframe = pandas.read_sql(selectQuery, pd_conn)
           dataframe.to_sql('booktb1', con=engine, if_exists='append')
           data = engine.execute("SELECT * FROM booktb1").fetchall()
           return render_template('AdminHome.html' , data=data)

       else:
        return render_template('index.html', error=error)


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():

    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = ibm_db.connect(dsn, "", "")
        pd_conn = ibm_db_dbi.Connection(conn)

        selectQuery = "SELECT * from regtb where UserName='" + username + "' and password='" + password + "'"
        dataframe = pandas.read_sql(selectQuery, pd_conn)

        if dataframe.empty:
            data1 = 'Username or Password is wrong'
            return render_template('goback.html', data=data1)
        else:
            print("Login")
            selectQuery = "SELECT * from regtb where UserName='" + username + "' and password='" + password + "'"
            dataframe = pandas.read_sql(selectQuery, pd_conn)

            dataframe.to_sql('Employee_Data',
                             con=engine,
                             if_exists='append')

            # run a sql query
            print(engine.execute("SELECT * FROM Employee_Data").fetchall())

            return render_template('UserHome.html', data=engine.execute("SELECT * FROM Employee_Data").fetchall())




@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':

        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        pnumber = request.form['phone']
        address = request.form['address']

        uname = request.form['uname']
        password = request.form['psw']

        conn = ibm_db.connect(dsn, "", "")

        insertQuery = "INSERT INTO regtb VALUES ('" + name1 + "','" + gender1 + "','" + Age + "','" + email + "','" + pnumber + "','" + address + "','" + uname + "','" + password + "')"
        insert_table = ibm_db.exec_immediate(conn, insertQuery)
        print(insert_table)



        # return 'file register successfully'


    return render_template('UserLogin.html')



@app.route("/newquery", methods=['GET', 'POST'])
def newquery():
    if request.method == 'POST':
        uname = session['uname']
        nitrogen = request.form['nitrogen']
        phosphorus = request.form['phosphorus']
        potassium = request.form['potassium']
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        ph = request.form['ph']
        rainfall = request.form['rainfall']
        location = request.form['select']

        nit = float(nitrogen)
        pho = float(phosphorus)
        po = float(potassium)
        te = float(temperature)
        hu = float(humidity)
        phh = float(ph)
        ra = float(rainfall)
        # age = int(age)

        filename = 'crop-prediction-rfc-model.pkl'
        classifier = pickle.load(open(filename, 'rb'))

        data = np.array([[nit, pho, po, te, hu, phh, ra]])
        my_prediction = classifier.predict(data)
        print(my_prediction)

        crop = ''
        fertilizer = ''

        if my_prediction == 0:
            Answer = 'Predict'
            crop = 'rice'

            fertilizer = '4 kg of gypsum and 1 kg of DAP/cent can be applied at 10 days after sowing'

        elif my_prediction == 1:
            Answer = 'Predict'
            crop = 'maize'
            fertilizer = 'The standard fertilizer recommendation for maize consists of 150 kg ha−1 NPK 14–23–14 and 50 kg ha−1 urea'
        elif my_prediction == 2:
            Answer = 'Predict'
            crop = 'chickpea'

            fertilizer = 'The generally recommended doses for chickpea include 20–30 kg nitrogen (N) and 40–60 kg phosphorus (P) ha-1. If soils are low in potassium (K), an application of 17 to 25 kg K ha-1 is recommended'

        elif my_prediction == 3:
            Answer = 'Predict'
            crop = 'kidneybeans'
            fertilizer = 'It needs good amount of Nitrogen about 100 to 125 kg/ha'

        elif my_prediction == 4:
            Answer = 'Predict'
            crop = 'pigeonpeas'
            fertilizer = 'Apply 25 - 30 kg N, 40 - 50 k g P 2 O 5 , 30 kg K 2 O per ha area as Basal dose at the time of sowing.'

        elif my_prediction == 5:
            Answer = 'Predict'
            crop = 'mothbeans'
            fertilizer = 'The applications of 10 kg N+40 kg P2O5 per hectare have proved the effective starter dose'
        elif my_prediction == 6:
            Answer = 'Predict'
            crop = 'mungbean'
            fertilizer = 'Phosphorus and potassium fertilizers should be applied at 50-50 kg ha-1'
        elif my_prediction == 7:
            Answer = 'Predict'
            crop = 'blackgram'
            fertilizer = 'The recommended fertilizer dose for black gram is 20:40:40 kg NPK/ha.'
        elif my_prediction == 8:
            Answer = 'Predict'
            crop = 'lentil'
            fertilizer = 'The recommended dose of fertilizers is 20kg N, 40kg P, 20 kg K and 20kg S/ha.'
        elif my_prediction == 9:
            Answer = 'Predict'
            crop = 'pomegranate'
            fertilizer = 'The recommended fertiliser dose is 600–700 gm of N, 200–250 gm of P2O5 and 200–250 gm of K2O per tree per year'

        elif my_prediction == 10:
            Answer = 'Predict'
            crop = 'banana'
            fertilizer = 'Feed regularly using either 8-10-8 (NPK) chemical fertilizer or organic composted manure'

        elif my_prediction == 11:
            Answer = 'Predict'
            crop = 'mango'
            fertilizer = '50 gm zinc sulphate, 50 gm copper sulphate and 20 gm borax per tree/annum are recommended'

        elif my_prediction == 12:
            Answer = 'Predict'
            crop = 'grapes'
            fertilizer = 'Use 3 pounds (1.5 kg.) of potassium sulfate per vine for mild deficiencies or up to 6 pounds (3 kg.)'

        elif my_prediction == 13:
            Answer = 'Predict'
            crop = 'watermelon'
            fertilizer = 'Apply a fertilizer high in phosphorous, such as 10-10-10, at a rate of 4 pounds per 1,000 square feet (60 to 90 feet of row)'

        elif my_prediction == 14:
            Answer = 'Predict'
            crop = 'muskmelon'
            fertilizer = 'Apply FYM 20 t/ha, NPK 40:60:30 kg/ha as basal and N @ 40 kg/ha 30 days after sowing.'

        elif my_prediction == 15:
            Answer = 'Predict'
            crop = 'apple'
            fertilizer = 'Apple trees require nitrogen, phosphorus and potassium,Common granular 20-10-10 fertilizer is suitable for apples'

        elif my_prediction == 16:
            Answer = 'Predict'
            crop = 'orange'
            fertilizer = 'Orange farmers often provide 5,5 – 7,7 lbs (2,5-3,5 kg) P2O5 in every adult tree for 4-5 consecutive years'

        elif my_prediction == 17:
            Answer = 'Predict'
            crop = 'papaya'
            fertilizer = 'Generally 90 g of Urea, 250 g of Super phosphate and 140 g of Muriate of Potash per plant are recommended for each application'

        elif my_prediction == 18:
            Answer = 'Predict'
            crop = 'coconut'
            fertilizer = 'Organic Manure @50kg/palm or 30 kg green manure, 500 g N, 320 g P2O5 and 1200 g K2O/palm/year in two split doses during September and May'

        elif my_prediction == 19:
            Answer = 'Predict'
            crop = 'cotton'
            fertilizer = 'N-P-K 20-10-10 per hectare during sowing (through the sowing machine)'

        elif my_prediction == 20:
            Answer = 'Predict'
            crop = 'jute'
            fertilizer = 'Apply 10 kg of N at 20 - 25 days after first weeding and then again on 35 - 40 days after second weeding as top dressing'

        elif my_prediction == 21:
            Answer = 'Predict'
            crop = 'coffee'
            fertilizer = 'Coffee trees need a lot of potash, nitrogen, and a little phosphoric acid. Spread the fertilizer in a ring around each Coffee plant'


        else:
            Answer = 'Predict'
            crop = 'Crop info not Found!'

        conn = ibm_db.connect(dsn, "", "")
        pd_conn = ibm_db_dbi.Connection(conn)

        insertQuery =  "INSERT INTO Querytb VALUES ('" + uname + "','" + nitrogen + "','" + phosphorus + "','" + potassium + "','"+temperature+"','"+humidity +"','"+ ph+"','"+ rainfall +"','Predict','"+ crop +"','"+fertilizer +"','"+location+"')"
        insert_table = ibm_db.exec_immediate(conn, insertQuery)
        print(insert_table)




        uname = session['uname']


        selectQuery = "SELECT * FROM Querytb where UserName='"+ uname+"'  "
        dataframe = pandas.read_sql(selectQuery, pd_conn)
        dataframe.to_sql('booktb1', con=engine, if_exists='append')
        data = engine.execute("SELECT * FROM booktb1").fetchall()






        return render_template('UserQueryAnswerinfo.html', wait=data)








@app.route("/AdminAinfo")
def AdminAinfo():

    conn = ibm_db.connect(dsn, "", "")
    pd_conn = ibm_db_dbi.Connection(conn)

    selectQuery = "SELECT * FROM Querytb   "
    dataframe = pandas.read_sql(selectQuery, pd_conn)
    dataframe.to_sql('booktb1', con=engine, if_exists='append')
    data = engine.execute("SELECT * FROM booktb1").fetchall()


    return render_template('AdminAnswer.html', data=data )




if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)