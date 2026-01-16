from flask import Flask, render_template, request, session, redirect,url_for
from werkzeug.utils import secure_filename

from mylib import *
import time
import os


app=Flask(__name__)

app.secret_key="super secret key"
app.config['UPLOAD_FOLDER']='./static/images'

#HOME


@app.route('/')
def home():
    return render_template('Welcome.html')
#LOGIN & LOGOUT & AUTH ERROR


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST" :
        email=request.form["T1"]
        password=request.form["T2"]
        cur=create_connection()
        sql="select * from logindata where email='"+email+"' AND password='"+password+"'"
        cur.execute(sql)
        n=cur.rowcount
        if n==1 :
            data=cur.fetchone()
            ut=data[2]
            #create session
            session["email"]=email
            session["usertype"]=ut
            if ut=="admin" :
                return redirect(url_for("admin_home"))
            elif ut=="accountant" :
                return redirect(url_for("accountant_home"))
            elif ut=="student":
                return redirect(url_for("student_home"))
            else:
                return render_template("Login.html",msg="contact to admin")
        else:
            return render_template("Login.html",msg="Either email or password is incorrect")
    else:
        return render_template("Login.html")


@app.route('/logout')
def logout():
    if "email" in session or "usertype" in session:
        session.pop("email")
        session.pop("usertype")
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/auth_error')
def auth_error():
    return render_template('AuthError.html')

#ADMIN
@app.route('/admin_home')
def admin_home():
    if "usertype" in session:
        email = session["email"]
        usertype = session["usertype"]
        if usertype == "admin":
            photo=check_photo(email)
            cur = create_connection()
            sql="select * from admindata where email='" + email + "'"
            cur.execute(sql)
            n=cur.rowcount
            if n == 1:
                data = cur.fetchone()
                return render_template("AdminHome.html", data=data,photo=photo)
            else:
                return render_template("AdminHome.html", msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route('/admin_reg', methods=['GET', 'POST'])
def admin_reg():
    if "usertype" in session:
        email = session["email"]
        usertype = session["usertype"]
        if usertype == "admin":
            if request.method == 'POST':
                print('This is a post request')
                #receive form data
                name=request.form['T1']
                contact=request.form['T2']
                email=request.form['T3']
                address=request.form['T4']
                password=request.form['T5']
                usertype="admin"
                cur = create_connection()
                s1="insert into admindata values('"+name+"','"+contact+"','"+email+"','"+address+"')"
                s2="insert into logindata values('"+email+"','"+password+"','"+usertype+"')"
                try:
                    cur.execute(s1)
                    n1=cur.rowcount
                    cur.execute(s2)
                    n2=cur.rowcount
                    if n1==1 and n2==1:
                        msg="Data saved and Login created"
                    elif n1==1:
                        msg="Only Data saved"
                    elif n2==1:
                        msg="Only Login created"
                    else:
                        msg="No Data saved and no Login created"

                except pymysql.err.IntegrityError:
                    msg="Already registered, use another email"
                return render_template('AdminReg.html', vgt=msg)
            else:
                #print("This is GET post")
                return render_template('AdminReg.html')
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route('/admin_profile', methods=['GET', 'POST'])
def admin_profile():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if ut=="admin":
            if request.method=="POST":
                cur=create_connection()
                name=request.form['T1']
                contact=request.form['T2']
                address=request.form['T3']
                sql="update admindata set name='"+name+"', contact=' "+contact+"', address='"+address+"'  where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('AdminProfile.html', msg="Data Saved")
                else:
                    return render_template('AdminProfile.html', msg="Data Not Saved")
            else:
                cur=create_connection()
                sql="select * from admindata where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template('AdminProfile.html', data=data)
                else:
                    return render_template('AdminProfile.html', msg="No Data Found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/show_admins')
def show_admins():
    if "email" in session:
        usertype=session["usertype"]
        if usertype=="admin":
            cur=create_connection()
            cur.execute("select * from admindata")
            if cur.rowcount>0:
                data=cur.fetchall()
                return render_template('AdminList.html',data=data)
            else:
                return render_template('AdminList.html',msg="No data found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/change_pass_admin', methods=['GET', 'POST'])
def change_pass_admin():
    if "email" in session:
        ut = session["usertype"]
        if ut == "admin":
            if request.method == 'POST':
                op=request.form['T1']
                np=request.form['T2']
                email=session["email"]
                cur = create_connection()
                sql="update logindata set password='"+np+"' where email='"+email+"'and password='"+op+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    msg="Password Changed Successfully"
                    return render_template('ChangePassAdmin.html', msg=msg)
                else:
                    msg="Password Not Changed"
                    return render_template('ChangePassAdmin.html', msg=msg)
            else:
                return render_template('ChangePassAdmin.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/adminphoto')
def adminphoto():
    return render_template('UploadAdminPhoto.html')

@app.route('/adminphoto1',methods=['GET','POST'])
def adminphoto1():
    if 'usertype' in session:
        ut=session['usertype']
        email=session['email']
        if ut=='admin':
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    path=os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time())) + '.' + file_ext
                    filename=secure_filename(filename)
                    cur=create_connection()
                    sql = "insert into photodata values('" + email + "','" + filename + "')"
                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            return render_template('UploadAdminPhoto1.html', result="success")
                        else:
                            return render_template('UploadAdminPhoto1.html', result="failure")
                    except:
                        return render_template('UploadAdminPhoto1.html', result="duplicate")
                else:
                    return redirect(url_for('adminphoto'))
            else:
                return render_template('UploadAdminPhoto.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/change_adminphoto')
def change_adminphoto():
    if 'usertype' in session:
        ut=session['usertype']
        email=session['email']
        if ut=='admin':
            photo = check_photo(email)
            cur = create_connection()
            sql = "delete from photodata where email='" + email + "'"
            cur.execute(sql)
            n = cur.rowcount
            if n > 0:
                os.remove("./static/images/" + photo)
                return render_template('ChangeAdminPhoto.html', data="success")
            else:
                return render_template('ChangeAdminPhoto.html', data="failure")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

#ACCOUNTANT
@app.route('/accountant_home')
def accountant_home():
    if "usertype" in session :
        e1=session["email"]
        ut=session["usertype"]
        if ut=="accountant" :
            cur = create_connection()
            sql="select * from accountantdata where email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n==1 :
                data=cur.fetchone()
                return render_template("AccountantHome.html",data=data)
            else:
                return render_template("AccountantHome.html",msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route('/accountant_reg', methods=['GET', 'POST'])
def accountant_reg():
    if "usertype" in session:
        e1 = session["email"]
        ut = session["usertype"]
        if ut == "admin":
            if request.method == 'POST':
                print('This is a post request')
                #receive form data
                name=request.form['T1']
                contact=request.form['T2']
                email=request.form['T3']
                address=request.form['T4']
                password=request.form['T5']
                usertype="accountant"
                cur = create_connection()
                s1="insert into accountantdata values('"+name+"','"+contact+"','"+email+"','"+address+"')"
                s2="insert into logindata values('"+email+"','"+password+"','"+usertype+"')"
                try:
                    cur.execute(s1)
                    n1=cur.rowcount
                    cur.execute(s2)
                    n2=cur.rowcount
                    if n1==1 and n2==1:
                        msg="Data saved and Login created"
                    elif n1==1:
                        msg="Only Data saved"
                    elif n2==1:
                        msg="Only Login created"
                    else:
                        msg="No Data saved and no Login created"

                except pymysql.err.IntegrityError:
                    msg="Already registered, use another email"
                return render_template('AccountantReg.html', vgt=msg)
            else:
                #print("This is GET post")
                return render_template('AccountantReg.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/accountant_profile', methods=['GET', 'POST'])
def accountant_profile():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if ut=="admin":
            if request.method=="POST":
                cur=create_connection()
                name=request.form['T1']
                contact=request.form['T2']
                address=request.form['T3']
                sql="update accountantdata set name='"+name+"', contact=' "+contact+"', address='"+address+"' where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('AccountantProfile.html', msg="Data Saved")
                else:
                    return render_template('AccountantProfile.html', msg="Data Not Saved")
            else:
                cur=create_connection()
                sql="select * from accountantdata where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template('AccountantProfile.html', data=data)
                else:
                    return render_template('AccountantProfile.html', msg="No Data Found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/show_accountants')
def show_accountants():
    if "email" in session:
        usertype=session["usertype"]
        if usertype=="admin":
            cur=create_connection()
            cur.execute("select * from accountantdata")
            if cur.rowcount>0:
                data=cur.fetchall()
                return render_template('AccountantList.html',data=data)
            else:
                return render_template('AccountantList.html',msg="No data found",data=None)
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/edit_accountant', methods=['GET', 'POST'])
def edit_accountant():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if ut== "admin":
            if request.method == 'POST':
                email=request.form['H1']
                cur=create_connection()
                sql="select * from accountantdata where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template('EditAccountant.html', vgt=data)
                else:
                    return render_template('EditAccountant.html', msg="No Data Found")
            else:
                return redirect(url_for('show_accountants'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/edit_accountant1', methods=['GET', 'POST'])
def edit_accountant1():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if ut== "admin":
            if request.method == 'POST':
                a=request.form['T1']
                contact=request.form['T2']
                email=request.form['T3']
                address = request.form['T4']
                cur=create_connection()
                sql="update accountantdata set name='"+a+"',contact='"+contact+"',address='"+address+"' where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    return render_template('EditAccountant1.html',msg="Data Updated")
                else:
                    return render_template('EditAccountant1.html',msg="No Changes Detected")
            else:
                return redirect(url_for('show_accountants'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/delete_accountant', methods=['GET', 'POST'])
def delete_accountant():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if ut=="admin":
            if request.method == 'POST':
                email=request.form['H1']
                cur = create_connection()
                sql="select * from accountantdata where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    data=cur.fetchone()
                    return render_template('DeleteAccountant.html', vgt=data)
                else:
                    return render_template('DeleteAccountant.html', msg="No Data Found")
            else:
                return redirect(url_for('show_accountants'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/delete_accountant1', methods=['GET', 'POST'])
def delete_accountant1():
    if "email" in session:
        ut=session["usertype"]
        if ut=="admin":
            if request.method == 'POST':
                email = request.form['T1']
                cur = create_connection()
                s1 = "delete from accountantdata where email='" + email + "'"
                s2 = "delete from logindata where email='" + email + "'"
                cur.execute(s1)
                cur.execute(s2)
                n1 = cur.rowcount
                n2 = cur.rowcount
                if n1==1 and n2==1:
                    return render_template('DeleteAccountant1.html', msg="Data Deleted")
                else:
                    return render_template('DeleteAccountant1.html', msg="No Data Found")
            else:
                return redirect(url_for('show_accountants'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/change_pass_accountant', methods=['GET', 'POST'])
def change_pass_accountant():
    if "email" in session:
        ut = session["usertype"]
        if ut == "accountant":
            if request.method == 'POST':
                op=request.form['T1']
                np=request.form['T2']
                email=session["email"]
                cur = create_connection()
                sql="update logindata set password='"+np+"' where email='"+email+"'and password='"+op+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    msg="Password changed successfully"
                    return render_template('ChangePassAccountant.html', msg=msg)
                else:
                    msg="Password not changed successfully"
                    return render_template('ChangePassAccountant.html', msg=msg)
            else:
                return render_template('ChangePassAccountant.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))
#STUDENTS
@app.route('/student_home')
def student_home():
    if "usertype" in session :
        e1=session["email"]
        ut=session["usertype"]
        if ut=="student" :
            cur = create_connection()
            sql="select * from studentdata where email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n==1 :
                data=cur.fetchone()
                return render_template("StudentHome.html",data=data)
            else:
                return render_template("StudentHome.html",msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if ut == "admin":
            if request.method == 'POST':
                email = request.form['H2']
                cur = create_connection()
                sql = "select * from studentdata where email='" + email + "'"
                cur.execute(sql)
                n = cur.rowcount
                if n > 0:
                    data = cur.fetchone()
                    return render_template('EditStudent.html', vgt=data)
                else:
                    return render_template('EditStudent.html', msg="No Data Found")
            else:
                return redirect(url_for('show_students_admin'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/edit_student1', methods=['GET', 'POST'])
def edit_student1():
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if ut == "admin":
            if request.method == 'POST':
                name = request.form['T1']
                gender = request.form['T2']
                joining_date = request.form['T3']
                father_name = request.form['T4']
                mother_name = request.form['T5']
                contact = request.form['T6']
                email = request.form['T7']
                address = request.form['T8']
                cur = create_connection()
                sql = "update studentdata set name='" + name + "',gender='" + gender + "',joining_date='" + joining_date + "',father_name='" + father_name + "',mother_name='" + mother_name + "',contact='" + contact + "',address='" + address + "' where email='" + email + "'"
                cur.execute(sql)
                n = cur.rowcount

                if n > 0:
                    return render_template('EditStudent1.html', msg="Data Updated")
                else:
                    return render_template('EditStudent1.html', msg="No Changes Detected")
            else:
                return redirect(url_for('show_students_admin'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/student_reg_admin', methods=['GET', 'POST'])
def student_reg_admin():
    if "usertype" in session:
        e1 = session["email"]
        ut = session["usertype"]
        if ut == "admin":
            if request.method == 'POST':
                name = request.form['T1']
                gender = request.form['T2']
                joining_date = request.form['T3']
                father_name = request.form['T4']
                mother_name = request.form['T5']
                contact = request.form['T6']
                email = request.form['T7']
                address = request.form['T8']
                usertype = "student"
                cur = create_connection()
                try:
                    s1 = "INSERT INTO studentdata (name, gender, joining_date, father_name, mother_name, contact, email, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    s2 = "INSERT INTO logindata (email, password, usertype) VALUES (%s, %s, %s)"
                    cur.execute(s1, (name, gender, joining_date, father_name, mother_name, contact, email, address))
                    cur.execute(s2, (email, joining_date, usertype))
                    cur.connection.commit()
                    msg = "Data saved and Login created"
                except pymysql.err.IntegrityError:
                    msg = "Already registered, use another email"
                return render_template('StudentRegAdmin.html', vgt=msg)
            else:
                return render_template('StudentRegAdmin.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/student_reg_accountant', methods=['GET', 'POST'])
def student_reg_accountant():
    if "usertype" in session:
        e1 = session["email"]
        ut = session["usertype"]
        if ut == "accountant":
            if request.method == 'POST':
                name = request.form['T1']
                gender = request.form['T2']
                joining_date = request.form['T3']
                father_name = request.form['T4']
                mother_name = request.form['T5']
                contact = request.form['T6']
                email = request.form['T7']
                address = request.form['T8']
                usertype = "student"
                cur = create_connection()
                try:
                    s1 = "INSERT INTO studentdata (name, gender, joining_date, father_name, mother_name, contact, email, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    s2 = "INSERT INTO logindata (email, password, usertype) VALUES (%s, %s, %s)"
                    cur.execute(s1, (name, gender, joining_date, father_name, mother_name, contact, email, address))
                    cur.execute(s2, (email, joining_date, usertype))
                    cur.connection.commit()
                    msg = "Data saved and Login created"
                except pymysql.err.IntegrityError:
                    msg = "Already registered, use another email"
                return render_template('StudentRegAccountant.html', vgt=msg)
            else:
                return render_template('StudentRegAccountant.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/show_students_admin')
def show_students_admin():
    if "email" in session:
        usertype=session["usertype"]
        if usertype=="admin":
            cur=create_connection()
            cur.execute("select * from studentdata")
            if cur.rowcount>0:
                data=cur.fetchall()
                return render_template('StudentListAdmin.html',student_portal=data)
            else:
                return render_template('StudentListAdmin.html',msg="No data found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/show_students_accountant')
def show_students_accountant():
    if "email" in session:
        usertype=session["usertype"]
        if usertype=="accountant":
            cur=create_connection()
            cur.execute("select * from studentdata")
            if cur.rowcount>0:
                data=cur.fetchall()
                return render_template('StudentListAccountant.html',student_portal=data)
            else:
                return render_template('StudentListAccountant.html',msg="No data found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/delete_student', methods=['GET', 'POST'])
def delete_student():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if ut=="admin":
            if request.method == 'POST':
                email=request.form['H1']
                cur = create_connection()
                sql="select * from studentdata where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    data=cur.fetchone()
                    return render_template('DeleteStudent.html', vgt=data)
                else:
                    return render_template('DeleteStudent.html', msg="No Data Found")
            else:
                return redirect(url_for('show_students_admin'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/delete_student1', methods=['GET', 'POST'])
def delete_student1():
    if "email" in session:
        ut=session["usertype"]
        if ut=="admin":
            if request.method == 'POST':
                email = request.form['T1']
                cur = create_connection()
                s1 = "delete from studentdata where email='" + email + "'"
                s2 = "delete from logindata where email='" + email + "'"
                cur.execute(s1)
                cur.execute(s2)
                n1 = cur.rowcount
                n2 = cur.rowcount
                if n1==1 and n2==1:
                    return render_template('DeleteStudent1.html', msg="Data Deleted")
                else:
                    return render_template('DeleteStudent1.html', msg="No Data Found")
            else:
                return redirect(url_for('show_students_admin'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/change_pass_student', methods=['GET', 'POST'])
def change_pass_student():
    if "email" in session:
        ut = session["usertype"]
        if ut == "student":
            if request.method == 'POST':
                op=request.form['T1']
                np=request.form['T2']
                email=session["email"]
                cur = create_connection()
                sql="update logindata set password='"+np+"' where email='"+email+"'and password='"+op+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    msg="Password changed successfully"
                    return render_template('ChangePassStudent.html', msg=msg)
                else:
                    msg="Password not changed successfully"
                    return render_template('ChangePassStudent.html', msg=msg)
            else:
                return render_template('ChangePassStudent.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/student_profile_admin', methods=['GET', 'POST'])
def student_profile_admin():
    if "usertype" in session:
        email = session["email"]
        usertype = session["usertype"]
        if usertype == "admin":
            if request.method == "POST":
                email=request.form['H1']
                cur = create_connection()
                sql1="select * from studentdata where email='" + email + "'"
                cur.execute(sql1)
                n1=cur.rowcount
                if n1 == 1:
                    data = cur.fetchone()

                    # This is for Courses
                    cur=create_connection()
                    id=request.form['H2']
                    sql2="select * from coursedata where student_id ='" + id + "'"
                    cur.execute(sql2)
                    result=cur.fetchall()
                    total=0
                    total_due=0
                    paid=0
                    course_data=[]
                    for d in result:
                        cr_paid=course_paid(id,d[0])

                        cr_due=int(d[4])-cr_paid
                        total=total+int(d[4])
                        total_due=total_due+cr_due
                        paid=paid+cr_paid
                        a=[d[0],d[1],d[2],d[3],d[4]]
                        a.append(cr_paid)
                        a.append(cr_due)
                        course_data.append(a)

                   #This is for Deposit
                    cur = create_connection()
                    id = request.form['H2']
                    sql3 = "select * from transactiondata where student_id ='" + id + "'"
                    cur.execute(sql3)
                    deposit= cur.fetchall()

                    return render_template("StudentProfileAdmin.html", data=data,result=course_data,deposit=deposit,total=total,total_due=total_due,paid=paid)
                else:
                    return render_template("StudentProfileAdmin.html", msg="Data Not Found")
            else:
                return render_template("StudentProfileAdmin.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route('/student_profile_accountant', methods=['GET', 'POST'])
def student_profile_accountant():
    if "usertype" in session:
        email = session["email"]
        usertype = session["usertype"]
        if usertype == "accountant":
            if request.method == "POST":
                email=request.form['H1']
                cur = create_connection()
                sql1="select * from studentdata where email='" + email + "'"
                cur.execute(sql1)
                n1=cur.rowcount
                if n1 == 1:
                    data = cur.fetchone()

                    # This is for Courses
                    cur=create_connection()
                    id=request.form['H2']
                    sql2="select * from coursedata where student_id ='" + id + "'"
                    cur.execute(sql2)
                    result=cur.fetchall()
                    total=0
                    total_due=0
                    paid=0
                    course_data=[]
                    for d in result:
                        cr_paid=course_paid(id,d[0])

                        cr_due=int(d[4])-cr_paid
                        total=total+int(d[4])
                        total_due=total_due+cr_due
                        paid=paid+cr_paid
                        a=[d[0],d[1],d[2],d[3],d[4]]
                        a.append(cr_paid)
                        a.append(cr_due)
                        course_data.append(a)

                   #This is for Deposit
                    cur = create_connection()
                    id = request.form['H2']
                    sql3 = "select * from transactiondata where student_id ='" + id + "'"
                    cur.execute(sql3)
                    deposit= cur.fetchall()

                    return render_template("StudentProfileAccountant.html", data=data,result=course_data,deposit=deposit,total=total,total_due=total_due,paid=paid)
                else:
                    return render_template("StudentProfileAccountant.html", msg="Data Not Found")
            else:
                return render_template("StudentProfileAccountant.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route('/student_profile_student', methods=['GET'])
def student_profile_student():

    if "usertype" in session and session["usertype"] == "student":
        email = session["email"]
        cur = create_connection()
        try:
            sql1 = "SELECT * FROM studentdata WHERE email = %s"
            cur.execute(sql1, (email,))
            if cur.rowcount == 1:
                data = cur.fetchone()
                student_id = data[0]
                sql2 = "SELECT * FROM coursedata WHERE student_id = %s"
                cur.execute(sql2, (student_id,))
                result = cur.fetchall()
                total = 0
                total_due = 0
                paid = 0
                course_data = []

                for d in result:

                    cr_paid = course_paid(student_id, d[0])

                    cr_due = int(d[4]) - cr_paid
                    total = total + int(d[4])
                    total_due = total_due + cr_due
                    paid = paid + cr_paid


                    a = [d[0], d[1], d[2], d[3], d[4]]
                    a.append(cr_paid)
                    a.append(cr_due)
                    course_data.append(a)


                sql3 = "SELECT * FROM transactiondata WHERE student_id = %s"
                cur.execute(sql3, (student_id,))
                deposit = cur.fetchall()


                return render_template("StudentProfileStudent.html",
                                       data=data,
                                       result=course_data,
                                       deposit=deposit,
                                       total=total,
                                       total_due=total_due,
                                       paid=paid)
            else:
                return render_template("StudentProfileStudent.html", msg="Student Data Not Found")

        except Exception as e:
            print(f"Error: {e}")
            return render_template("StudentProfileStudent.html", msg="An error occurred")

    else:
        return redirect(url_for("auth_error"))


@app.route('/deposit',methods=['GET', 'POST'])
def deposit():
    if "usertype" in session:
        email = session["email"]
        usertype = session["usertype"]
        if usertype == "admin":
            if request.method == "POST":
                student_id=request.form['H1']
                student_name=request.form['H2']
                course_id=request.form['H3']
                course_name=request.form['H4']
                print(course_name)
                return render_template("DepositAdmin.html",student_id=student_id,student_name=student_name, course_id=course_id,course_name=course_name)
            else:
                return render_template("DepositAdmin.html", msg="GET")
        elif usertype == "accountant":
            if request.method == "POST":
                student_id = request.form['H1']
                student_name = request.form['H2']
                course_id = request.form['H3']
                course_name = request.form['H4']
                print(course_name)
                return render_template("DepositAccountant.html", student_id=student_id, student_name=student_name,
                                       course_id=course_id, course_name=course_name)
            else:
                return render_template("DepositAccountant.html", msg="GET")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route('/deposit1', methods=['GET', 'POST'])
def deposit1():
    if "usertype" in session:
        email = session["email"]
        usertype = session["usertype"]
        if usertype == "admin":
            if request.method == "POST":
                student_id=request.form['H1']
                email=get_student_email(student_id)
                student_name=request.form['H2']
                course_id=request.form['H3']
                course_name=request.form['H4']
                deposit_amount=request.form['T2']
                deposit_date=request.form['T3']
                payment_method=request.form['T4']
                cur = create_connection()
                sql="insert into transactiondata values(0,'"+student_id+"','"+student_name+"','"+course_id+"','"+course_name+"','"+deposit_amount+"','"+deposit_date+"','"+payment_method+"')"
                cur.execute(sql)
                n = cur.rowcount
                if n >0:
                    msg="Deposit Successful"
                    return render_template("DepositAdmin.html", msg=msg,email=email,student_id=student_id)
                else:
                    msg="Deposit Failed"
                    return render_template("DepositAdmin.html", msg=msg,email=email,student_id=student_id)
            else:
                return render_template("DepositAdmin.html", msg="GET")
        elif usertype == "accountant":
            if request.method == "POST":
                student_id = request.form['H1']
                email = get_student_email(student_id)
                student_name = request.form['H2']
                course_id = request.form['H3']
                course_name = request.form['H4']
                deposit_amount = request.form['T2']
                deposit_date = request.form['T3']
                payment_method = request.form['T4']
                cur = create_connection()
                sql = "insert into transactiondata values(0,'" + student_id + "','" + student_name + "','" + course_id + "','" + course_name + "','" + deposit_amount + "','" + deposit_date + "','" + payment_method + "')"
                cur.execute(sql)
                n = cur.rowcount
                if n > 0:
                    msg = "Deposit Successful"
                    return render_template("DepositAccountant.html", msg=msg, email=email, student_id=student_id)
                else:
                    msg = "Deposit Failed"
                    return render_template("DepositAccountant.html", msg=msg, email=email, student_id=student_id)
            else:
                return render_template("DepositAccountant.html", msg="GET")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route('/add_course',methods=['GET', 'POST'])
def add_course():
    if "usertype" in session:
        email = session["email"]
        usertype = session["usertype"]
        if usertype == "admin":
            if request.method == "POST":
                student_id=request.form['H1']
                student_name=request.form['H2']
                return render_template("AddCourseAdmin.html",id=student_id,name=student_name)
            else:
                return render_template("AddCourseAdmin.html")
        elif usertype == "accountant":
            if request.method == "POST":
                student_id=request.form['H1']
                student_name=request.form['H2']
                return render_template("AddCourseAccountant.html",id=student_id,name=student_name)
            else:
                return render_template("AddCourseAccountant.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route('/add_course1',methods=['GET', 'POST'])
def add_course1():
    if "usertype" in session:
        email = session["email"]
        usertype = session["usertype"]
        if usertype == "admin":
            if request.method == "POST":
                student_id=request.form['H1']
                student_name=request.form['H2']
                course_name=request.form['T4']
                course_fees=request.form['T5']
                cur = create_connection()
                sql="insert into coursedata values(0,'"+student_id+"','"+student_name+"','"+course_name+"','"+course_fees+"')"
                try:
                    cur.execute(sql)
                    n=cur.rowcount
                    if n==1:
                        msg="Course Added"
                    else:
                        msg="Course Not Added"
                except pymysql.err.IntegrityError:
                    msg="Course Already Exists"
                return render_template("AddCourseAdmin.html",msg=msg)
            else:
                return render_template("AddCourseAdmin.html")
        elif usertype == "accountant":
            if request.method == "POST":
                student_id = request.form['H1']
                student_name = request.form['H2']
                course_name = request.form['T4']
                course_fees = request.form['T5']
                cur = create_connection()
                sql = "insert into coursedata values(0,'" + student_id + "','" + student_name + "','" + course_name + "','" + course_fees + "')"
                try:
                    cur.execute(sql)
                    n = cur.rowcount
                    if n == 1:
                        msg = "Course Added"
                    else:
                        msg = "Course Not Added"
                except pymysql.err.IntegrityError:
                    msg = "Course Already Exists"
                return render_template("AddCourseAccountant.html", msg=msg)
            else:
                return render_template("AddCourseAccountant.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route('/delete_course',methods=['GET', 'POST'])
def delete_course():
    if "usertype" in session:
        email = session["email"]
        usertype = session["usertype"]
        if usertype == "admin":
            if request.method == "POST":
                id=request.form['H1']
                cur = create_connection()
                sql = "select * from coursedata where course_id='" + id + "'"
                cur.execute(sql)
                n = cur.rowcount
                if n > 0:
                    data = cur.fetchone()
                    return render_template("DeleteCourseAdmin.html", data=data)
                else:
                    return render_template("DeleteCourseAdmin.html", msg="No data found")
            else:
                return redirect(url_for("student_profile_admin"))
        elif usertype == "accountant":
            if request.method == "POST":
                id = request.form['H1']
                cur = create_connection()
                sql = "select * from coursedata where course_id='" + id + "'"
                cur.execute(sql)
                n = cur.rowcount
                if n > 0:
                    data = cur.fetchone()
                    return render_template("DeleteCourseAccountant.html", data=data)
                else:
                    return render_template("DeleteCourseAccountant.html", msg="No data found")
            else:
                return redirect(url_for("student_profile_accountant"))

        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route('/delete_course1',methods=['GET', 'POST'])
def delete_course1():
    if "usertype" in session:
        email = session["email"]
        usertype = session["usertype"]
        if usertype == "admin":
            if request.method == "POST":
                id=request.form['H1']
                cur = create_connection()
                sql="delete from coursedata where course_id='" + id + "'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    msg="Course Deleted"
                    return render_template("DeleteCourseAdmin.html", msg=msg)
                else:
                    msg="Course Not Deleted"
                    return render_template("DeleteCourseAdmin.html", msg=msg)
            else:
                course_id=request.form['H1']
                cur = create_connection()
                sql="select * from coursedata where course_id='"+course_id+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template("DeleteCourseAdmin.html", data=data)
                else:
                    return render_template("DeleteCourseAdmin.html", msg="Data Not Found")
        elif usertype == "accountant":
            if request.method == "POST":
                course_id=request.form['H1']
                cur = create_connection()
                sql="delete from coursedata where course_id='" + course_id + "'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    msg="Course Deleted"
                    return render_template("DeleteCourseAccountant.html", msg=msg)
                else:
                    msg="Course Not Deleted"
                    return render_template("DeleteCourseAccountant.html", msg=msg)
            else:
                course_id = request.form['H1']
                cur = create_connection()
                sql = "select * from coursedata where course_id='" + course_id + "'"
                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                    data = cur.fetchone()
                    return render_template("DeleteCourseAccountant.html", data=data)
                else:
                    return render_template("DeleteCourseAccountant.html", msg="Data Not Found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))







@app.route('/show_courses')
def show_courses():
    if "usertype" in session:
        email = session["email"]
        usertype = session["usertype"]
        if usertype == "admin":
            cur = create_connection()
            sql="select * from coursedata"
            cur.execute(sql)
            n = cur.rowcount
            if n >0:
                data = cur.fetchall()
                return render_template("ShowCourses.html",data=data)
            else:
                msg="Course Not Found"
                return render_template("ShowCourses.html",msg=msg)
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))






@app.route('/show_transaction')
def show_transaction():
    if "usertype" in session:
        email = session["email"]
        usertype = session["usertype"]
        if usertype == "admin":
            cur = create_connection()
            sql="select * from transactiondata"
            cur.execute(sql)
            n = cur.rowcount
            if n >0:
                data = cur.fetchall()
                return render_template("ShowTransactionAdmin.html",data=data)
            else:
                msg="Course Not Found"
                return render_template("ShowTransactionAdmin.html",msg=msg)
        elif usertype == "accountant":
            cur = create_connection()
            sql="select * from transactiondata"
            cur.execute(sql)
            n = cur.rowcount
            if n >0:
                data = cur.fetchall()
                return render_template("ShowTransactionAccountant.html",data=data)
            else:
                msg="Course Not Found"
                return render_template("ShowTransactionAcc.html",msg=msg)
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))









#QUICK LINKS

@app.route('/courses')
def courses():
    return render_template('CoursesList.html')



if __name__ == '__main__':
    app.run(debug=True)