from flask import Flask, render_template, request, redirect, url_for, session,flash,jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from threading import Thread
from time import sleep

app = Flask(__name__)

app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ronaldo@123'
app.config['MYSQL_DB'] = 'printingdb'

  
mysql = MySQL(app)

try:
    mysql.session.ping()
    print("Database connected!")
except Exception as e:
    print("Error connecting to database:", e)

@app.route('/')
def log():
 return render_template('login.html')

@app.route('/Login', methods=['POST'])
def Login():
    username = request.form['username']
    password = request.form['password']
    user_type = request.form['user_type']

    # Your authentication code here
    if user_type == 'admin' and username == 'admin123@gmail.com' and password == 'admin123':
        return render_template('admin_dashboard.html')
    elif user_type == 'cashier' and username == 'cashier123@gmail.com' and password == 'cashier123':
        return render_template('cashier_dashboard.html')
    else:
        return render_template('Login.html', message='Invalid credentials')

    
@app.route('/admin_dashboard')
def dashboard():
     return render_template('admin_dashboard.html') 

    
@app.route('/cashier_dashboard')
def cashier_dashboard():
     return render_template('cashier_dashboard.html') 


@app.route('/add_item', methods =['GET', 'POST'])
def add_item():
    message = ''
    if request.method == 'POST' and 'item_id' in request.form and 'item_name' in request.form and 'item_price' in request.form and 'tax_without_price'  in request.form and 'total_price'  in request.form:
        itemid = request.form['item_id']
        itemname = request.form['item_name']
        itemprice = request.form['item_price']
        taxwithoutprice=request.form['tax_without_price']
        totalprice=request.form['total_price']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Item WHERE Item_ID = % s', (itemid, ))
        Item = cursor.fetchone()
        if not itemid or not itemname or not itemprice or not taxwithoutprice or not totalprice:
            message = 'Please fill out form !'
        elif Item:
            message = 'Item already exist !'
        else:
            cursor.execute('INSERT INTO Item VALUES (% s, % s, % s,% s, %s)', (itemid, itemname, itemprice,taxwithoutprice,totalprice))
            mysql.connection.commit()
            message = 'Item Added Successfully !'
    elif request.method == 'POST':
        message = 'Please fill out the Item form !'
    return render_template('additem.html', message = message)



@app.route('/calculation', methods=['GET', 'POST'])
def calculation():
    if request.method == 'POST':
        input_1 = request.form.get('pages_number')
        input2 = request.form.get('input2')
        input3 = request.form.get('input3')
        input4 = request.form.get('input4')
        input5 = request.form.get('input5')
        input6 = request.form.get('input6')
        input7 = request.form.get('input7')

        if not input_1:
            flash('Please enter the number of pages.')
            return redirect(request.url)
        
        try:
            pages_number = float(input_1)
        except ValueError:
            flash('Please enter a valid number for the number of pages.')
            return redirect(request.url)

        if pages_number < 6:
            result = 2.00
        elif pages_number < 11:
            result = 3.00
        elif pages_number < 16:
            result = 4.00
        elif pages_number < 21:
            result = 5.00
        elif pages_number < 26:
            result = 6.00
        elif pages_number < 31:
            result = 7.00
        elif pages_number < 36:
            result = 8.00
        elif pages_number < 41:
            result = 9.00
        elif pages_number < 46:
            result = 10.00
        elif pages_number < 251:
            result = pages_number / 4
        elif pages_number < 501:
            result = pages_number / 5
        elif pages_number < 801:
            result = pages_number / 6
        elif pages_number < 1001:
            result = pages_number / 7
        elif pages_number < 50000:
            result = pages_number / 8
        else:
            result = None

        # Convert to string and remove leading and trailing zeros
        number_str = '{:.10f}'.format(result).rstrip('0').rstrip('.')
        result2 = round(float(number_str))
        result3 = result * 0.15
        rounded_result3 = round(result3, 2)
        result5 = result2 + rounded_result3
        result6 = result / pages_number
        result7 = result5 / pages_number
        rounded_result7 = round(result7, 2)

        return render_template('Calculation.html', input_1=int(pages_number), input2="{:.2f}".format(result),
                               input3=result2, input4="{:.2f}".format(rounded_result3),
                               input5="{:.2f}".format(result5), input6="{:.2f}".format(result6),
                               input7=rounded_result7)

    return render_template('Calculation.html')

  
  #####################Second Calculation Function is start from here.################
@app.route('/calculation2',methods=['GET','POST'])
def calculation2():
    if request.method=='POST':
        input_1_malon = request.form.get('pages_number_malon')
        input2_malon = request.form.get('input2_malon')
        input3_malon=request.form.get('input3_malon')
        input4_malon=request.form.get('input4_malon')
        input5_malon=request.form.get('input5_malon')
        input6_malon=request.form.get('input6_malon')
        input7_malon=request.form.get('input7_malon')
        page_number_malon=float(input_1_malon)

        if not input_1_malon:
            flash('Please enter the number of pages.')
            return redirect(request.url)
        
        try:
            page_number_malon = float(input_1_malon)
        except ValueError:
            flash('Please enter a valid number for the number of pages.')
            return redirect(request.url)

        if page_number_malon < 2:
            result = 4
        elif page_number_malon < 3:
            result = 6
        elif page_number_malon < 4:
            result = 8
        elif page_number_malon < 5:
            result = 10
        elif page_number_malon < 6:
            result = 12
        elif page_number_malon < 7:
            result = 14
        elif page_number_malon < 8:
            result = 16
        elif page_number_malon < 9:
            result = 18
        elif page_number_malon < 10:
            result = 20
        elif page_number_malon < 11:
            result = 22.00
        elif page_number_malon < 12:
            result = 24
        elif page_number_malon < 13:
            result = 26
        elif page_number_malon < 14:
            result = 28
        elif page_number_malon < 15:
            result = 30
        elif page_number_malon < 16:
            result = 32
        elif page_number_malon < 17:
            result = 34
        elif page_number_malon < 18:
            result = 36
        elif page_number_malon < 19:
            result = 38
        elif page_number_malon < 20:
            result = 40
        elif page_number_malon < 21:
            result = 42
        elif page_number_malon < 26:
            result = 1.8 * page_number_malon
        elif page_number_malon < 31:
            result = 1.7 * page_number_malon
        elif page_number_malon < 36:
            result = 1.6 * page_number_malon
        elif page_number_malon < 41:
            result = 1.5 * page_number_malon
        elif page_number_malon < 46:
            result = 1.4 * page_number_malon
        elif page_number_malon < 51:
            result = 1.1 * page_number_malon
        else:
            result = 1 * page_number_malon
 

    # Convert to string and remove leading and trailing zeros
    number_str_malon = '{:.10f}'.format(result).rstrip('0').rstrip('.')
    result2_malon = round(float(number_str_malon))
    result3_malon=result*0.15
    rounded_result3_malon=round(result3_malon,2)
    result5_malon=result2_malon+rounded_result3_malon
    result6_malon=result/page_number_malon
    result7_malon=result5_malon/page_number_malon
    rounded_result7_malon=round(result7_malon,2)


    print(page_number_malon,"  " , "{:.2f}".format(result) , " " , result2_malon , " " , rounded_result3_malon , " " , result5_malon , " " , result6_malon, " " , rounded_result7_malon)
    return render_template('Calculation.html' ,  input_1_malon = int(page_number_malon), input2_malon="{:.2f}".format(result) , input3_malon="{:.2f}".format(result2_malon),
                           input4_malon="{:.2f}".format(result3_malon) , input5_malon="{:.2f}".format(result5_malon) , input6_malon=round(result6_malon,2) , input7_malon=rounded_result7_malon)




#####################Third Calculation Function is start from here.################


@app.route('/calculation3',methods=['POST','GET'])
def calculation3():
    if request.method == 'POST':
        input_1_alsur = request.form.get('pages_number_alsur')
        input2_malon = request.form.get('input2_alsur')
        input3_alsur=request.form.get('input3_alsur')
        input4_alsur=request.form.get('input4_alsur')
        input5_alsur=request.form.get('input5_alsur')
        input6_alsur=request.form.get('input6_alsur')
        input7_alsur=request.form('input7_alsur')
        page_number_alsur=float(input_1_alsur)

        
        if not input_1_alsur:
            flash('Please enter the number of pages.')
            return redirect(request.url)
        
        try:
            page_number_alsur = float(input_1_alsur)
        except ValueError:
            flash('Please enter a valid number for the number of pages.')
            return redirect(request.url)
        
        if page_number_alsur < 21:
            result = 2 * page_number_alsur
        elif page_number_alsur < 50:
            result = 1.9 * page_number_alsur
        else:
            result = None  # Or you can set a default value for cases when pages_number_alsur >= 50

        # Convert to string and remove leading and trailing zeros
        number_str_alsur = '{:.10f}'.format(result).rstrip('0').rstrip('.')
        result2_alsur = round(float(number_str_alsur))
        result3_alsur=result*0.15
        rounded_result3_alsur=round(result3_alsur,2)
        result5_alsur=result2_alsur+rounded_result3_alsur
        result6_alsur=result/page_number_alsur
        result7_alsur=result5_alsur/page_number_alsur
        rounded_result7_alsur=round(result7_alsur,2)


    print(page_number_alsur,"  " , "{:.2f}".format(result) , " " , result2_alsur , " " , rounded_result3_alsur , " " , result5_alsur , " " , result6_alsur, " " , rounded_result7_alsur)
    return render_template('Calculation.html' ,  input_1_alsur = int(page_number_alsur), input2_alsur=round(result) , input3_alsur=result2_alsur,
                           input4_alsur=round(result3_alsur) , input5_alsur=round(result5_alsur) , input6_alsur="{:.2f}".format(result6_alsur) , input7_alsur="{:.4f}".format(result7_alsur) )

#################################Calculation Fourth start from here############


@app.route('/calculation4',methods=['POST','GET'])
def calculation4():
    if request.method=='POST':
        input_1_wahid = request.form.get('pages_number_wahid')
        input2_malon = request.form.get('input2_wahid')
        input3_wahid=request.form.get('input3_wahid')
        input4_wahid=request.form.get('input4_wahid')
        input5_wahid=request.form.get('input5_wahid')
        input6_wahid=request.form.get('input6_wahid')
        input7_wahid=request.form.get('input7_wahid')

         
        if not input_1_wahid:
            flash('Please enter the number of pages.')
            return redirect(request.url)
        
        try:
            page_number_wahid = float(input_1_wahid)
        except ValueError:
            flash('Please enter a valid number for the number of pages.')
            return redirect(request.url)

        page_number_wahid=float(input_1_wahid)
        if page_number_wahid < 51:
            result = 5 * page_number_wahid
        elif page_number_wahid < 101:
            result = 4.7 * page_number_wahid
        elif page_number_wahid < 5000:
            result = 4 * page_number_wahid
        else:
            result = None  # or set a default value for pages_wahid >= 5000

        # Convert to string and remove leading and trailing zeros
        number_str_wahid = '{:.10f}'.format(result).rstrip('0').rstrip('.')
        result2_wahid = round(float(number_str_wahid))
        result3_wahid=result+0.15
        rounded_result3_wahid=round(result3_wahid,2)
        result5_wahid=result2_wahid+rounded_result3_wahid
        result6_wahid=result/page_number_wahid
        result7_wahid=result5_wahid/page_number_wahid
        rounded_result7_wahid=round(result7_wahid,2)


    print(page_number_wahid,"  " , "{:.2f}".format(result) , " " , result2_wahid , " " , rounded_result3_wahid , " " , result5_wahid , " " , result6_wahid, " " , rounded_result7_wahid)
    return render_template('Calculation.html' ,  input_1_wahid = int(page_number_wahid), input2_wahid="{:.2f}".format(result) , input3_wahid="{:.2f}".format(result2_wahid),
                           input4_wahid="{:.2f}".format(result3_wahid) , input5_wahid="{:.2f}".format(result5_wahid), input6_wahid="{:.2f}".format(result6_wahid) , input7_wahid="{:.2f}".format(result7_wahid) )



@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('log'))


if __name__ == '__main__':
    app.run(debug=True)
