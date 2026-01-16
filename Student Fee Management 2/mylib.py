import pymysql
def create_connection():
    con=pymysql.connect(host="localhost",user="root",port=3306,db="student_portal",passwd="",autocommit=True)
    cur=con.cursor()
    return cur

def course_paid(sid,cid):
    cur=create_connection()
    sql="select * from transactiondata where student_id ='"+str(sid)+"' and course_id='"+str(cid)+"'"
    print(sql)
    cur.execute(sql)
    total=0
    n=cur.rowcount
    if(n>0):
        data=cur.fetchall()
        print(data)
        for d in data:
            total=total+int(d[5])
    print(total)
    return total
def get_student_email(sid):
    cur=create_connection()
    sql="select * from studentdata where id ='"+str(sid)+"'"
    print(sql)
    cur.execute(sql)
    n=cur.rowcount
    email=None
    if(n>0):
        data=cur.fetchone()
        email=data[7]
    return email



def check_photo(email):
    cur =  create_connection()
    sql="SELECT * FROM photodata where email='" + email + "'"
    cur.execute(sql)
    print(sql)
    n=cur.rowcount
    photo="no"
    if n>0:
        row=cur.fetchone()
        photo=row[1]
    print("check_photo",photo)
    return photo