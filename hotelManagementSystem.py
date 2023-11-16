import pymysql
import matplotlib.pyplot as plt
import pandas as pd

#░█▀▀▀ ░█─░█ ░█▄─░█ ░█▀▀█ ░█▀▀▀█ 　 ░█▀▀▀ ░█▀▀▀█ ░█▀▀█ 　 ░█▀▀█ ░█─░█ ░█▀▀▀ ░█▀▀▀█ ▀▀█▀▀ 
#░█▀▀▀ ░█─░█ ░█░█░█ ░█─── ─▀▀▀▄▄ 　 ░█▀▀▀ ░█──░█ ░█▄▄▀ 　 ░█─▄▄ ░█─░█ ░█▀▀▀ ─▀▀▀▄▄ ─░█── 
#░█─── ─▀▄▄▀ ░█──▀█ ░█▄▄█ ░█▄▄▄█ 　 ░█─── ░█▄▄▄█ ░█─░█ 　 ░█▄▄█ ─▀▄▄▀ ░█▄▄▄ ░█▄▄▄█ ─░█──

def guest():
    print()
    print("1. Show all the records of guest \n2. Add records of guest \n3. Search records \n4. Delete records of guest \n5. Graphical representation \n6. Update the records")
    x=int(input("Enter the no. "))
    print()
    if x==1:
        g_showrecords()
    elif x==2:
        g_addrecords()   
    elif x==3:
        g_search()
    elif x==4:
        g_delete()
    elif x==5:
        g_graphics()
    elif x==6:
        g_updaterecords()
    else:
        print("INVALID INPUT")

def g_showrecords():
    d1=pymysql.connect(host="localhost",user="root",passwd="root",database="hotel")
    #c1=d1.cursor()
    quer="select * from guest;"
    df=pd.read_sql(quer,d1)
    print(df)
 
def g_addrecords():
    d1=pymysql.connect(host="localhost",user="root",passwd="root",database="hotel")
    c1=d1.cursor()
    guestid = int(input("Guest id: "))
    nameofguest = input("Name of guest: ")
    type_of_room = input("Type of room single or double or triple or quad: ")
    nofdays = int(input("No of days: "))
    cidate = input("Check in date in yyyy-mm-dd: ")
    codate = input("Check out date in yyyy-mm-dd: ")
    room_no = int(input("Room no: "))
    source_of_booking = input("Source of booking online or offline: ")
    netpay = int(input("Netpay: "))

    val = (guestid, nameofguest, type_of_room, 
          nofdays, cidate, codate, room_no, source_of_booking, netpay)

    quer="INSERT INTO guest(guestid, nameofguest, type_of_room, nofdays, cidate, codate, room_no, source_of_booking, netpay) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);" 
    print(c1.execute(quer,val))
    d1.commit()
    print("Record Added")

def g_search():
    d1=pymysql.connect(user="root",host="localhost",passwd="root",database="hotel")
    #c1=d1.cursor() 
    x=int(input("Guest id: "))
    quer="select * from guest where guestid=" + str(x)
    df=pd.read_sql(quer,d1)
    if df.size!=0:
        print(df)
    else:
        print("Guest ", x, "isn't present")

def g_delete():
    d1=pymysql.connect(host="localhost",user="root",passwd="root",database="hotel")
    c1=d1.cursor()   
    x=int(input("Enter the id: "))
    quer="delete from guest where guestid=%d;" %x
    rowcount=c1.execute(quer)
    if rowcount>0:
        d1.commit()
        print("Record Deleted")
    else:
        print("NO RECORD FOUND")

def g_graphics():
    d1=pymysql.connect(host="localhost",user="root",passwd="root",database="hotel")
    #c1=d1.cursor()     
    print("1. Rooms booked \n2. Source of booking")
    x=int(input("enter the no:"))
    if x==1:
        g_roomgraph()
    elif x==2:
        g_sobgraph()
    else:
        print("INVAILD INPUT")   

def g_roomgraph():
    d1=pymysql.connect(host="localhost",user="root",passwd="root",database="hotel")
    c1=d1.cursor()   
    quer='''select count(*) from guest where type_of_room="single";'''
    c1.execute(quer)
    x=c1.fetchone()
    lst=list(x)
    quer='''select count(*) from guest where type_of_room="double";'''
    c1.execute(quer)
    y=c1.fetchone()
    lst1=list(y)
    quer='''select count(*) from guest where type_of_room="triple";'''
    c1.execute(quer)
    z=c1.fetchone()
    lst2=list(z)
    quer='''select count(*) from guest where type_of_room="quad";'''
    c1.execute(quer)
    a=c1.fetchone()
    lst3=list(a)
    lstt=lst+lst1+lst2+lst3
    y=["single","double","triple","quad"]
    plt.bar(y,lstt,width=0.50)
    plt.xlabel("Types of Rooms")
    plt.ylabel("No.of Rooms")
    plt.title("Room graph")
    plt.show()     

def g_sobgraph():
    d1=pymysql.connect(host="localhost",user="root",passwd="root",database="hotel")
    c1=d1.cursor()
    quer='select count(*) from guest where source_of_booking="online";'
    c1.execute(quer)
    x=c1.fetchone()
    lst=list(x)
    quer="select count(*) from guest where source_of_booking='offline';"
    c1.execute(quer)
    y=c1.fetchone()
    lst1=list(y)
    lstt=lst+lst1
    y=["online","offline"]
    plt.bar(y,lstt,width=0.50)
    plt.xlabel("Source of Booking")
    plt.ylabel("No.of Rooms")
    plt.title("Source of Booking graph")
    plt.show()

def g_updaterecords():
    d1=pymysql.connect(user="root",host="localhost",passwd="root",database="hotel")
    c1=d1.cursor()
    gid=int(input("Enter the id of whomever you want to update the record of: "))
    quer="select * from guest where guestid=%d" % gid
    c1.execute(quer)
    if c1.rowcount>0:
        #row=list(c1.fetchone())
        df=pd.read_sql(quer,d1)
        print(df)
        print("\n1. Name of guest \n2. Source of booking \n3. Check in date \n4. Check out date \n5. No. of days \n6. Room no.  \n7. Netpay \n8. Type of room")
        cr=int(input("Enter the no: "))

        #Name of guest
        if cr==1:
            y=input("Enter the new name of guest: ")
            quer="update guest set nameofguest='%s' where guestid=%d" %(y,gid)
            c1.execute(quer)
            d1.commit()
            print("Record Updated")
        #Source of booking             
        elif cr==2:
            y=input("Enter the new source of booking: ")
            quer="update guest set source_of_booking='%s' where guestid=%d" %(y,gid)
            c1.execute(quer)
            d1.commit()
            print("Record Updated") 
        #Check in date                 
        elif cr==3:
            y=input("Enter the new check in date yyyy-mm-dd: ")
            quer="update guest set cidate='%s' where guestid=%d" %(y,gid)
            c1.execute(quer)
            d1.commit()
            print("Record Updated")
        #Check out date    
        elif cr==4:
            y=input("Enter the new check out date yyyy-mm-dd: ")
            quer="update guest set codate='%s' where guestid=%d" %(y,gid)
            c1.execute(quer)
            d1.commit()
            print("Record Updated")   
        #No. of days     
        elif cr==5:
            y=input("Enter the new no. of days: ")
            quer="update guest set nofdays='%s' where guestid=%d" %(y,gid)
            c1.execute(quer)
            d1.commit()
            print("Record Updated")
        #Room no.     
        elif cr==6:
            y=input("Enter the new room no: ")
            quer="update guest set room_no='%s' where guestid=%d" %(y,gid)
            c1.execute(quer)
            d1.commit()
            print("Record Updated")
        #Netpay    
        elif cr==7:
            y=input("Enter the new netpay: ")
            quer="update guest set netpay='%s' where guestid=%d" %(y,gid)
            c1.execute(quer)
            d1.commit()
            print("Record Updated")
        #Type of room            
        elif cr==8:
            y=input("Type of room single or double or triple or quad: ") 
            quer="update guest set type_of_room='%s' where guestid='%d'" %(y,gid)
            c1.execute(quer)
            d1.commit()
            print("Record Updated")   
    elif c1.rowcount==0 or c1!=[1,2,3,4,5,6,7,8]:
        print("NO RECORD FOUND TO CHANGE")

#░█▀▀▀ ░█─░█ ░█▄─░█ ░█▀▀█ ░█▀▀▀█ 　 ░█▀▀▀ ░█▀▀▀█ ░█▀▀█ 　 ░█▀▀▀█ ▀▀█▀▀ ─█▀▀█ ░█▀▀▀ ░█▀▀▀ 
#░█▀▀▀ ░█─░█ ░█░█░█ ░█─── ─▀▀▀▄▄ 　 ░█▀▀▀ ░█──░█ ░█▄▄▀ 　 ─▀▀▀▄▄ ─░█── ░█▄▄█ ░█▀▀▀ ░█▀▀▀ 
#░█─── ─▀▄▄▀ ░█──▀█ ░█▄▄█ ░█▄▄▄█ 　 ░█─── ░█▄▄▄█ ░█─░█ 　 ░█▄▄▄█ ─░█── ░█─░█ ░█─── ░█───

def staff():
    print()
    print("\n1. Show all the records of staff \n2. Add records of staff \n3. Search records of staff \n4. Delete records of staff \n5. Graphical representation \n6. Update the records") 
    x=int(input("Enter the no. "))
    print()
    if x==1:
        s_showrecords()
    elif x==2:
        s_addrecords()   
    elif x==3:
        s_search()
    elif x==4:
        s_delete()
    elif x==5:
        s_graphics()
    elif x==6:
        s_updaterecords()
    else:
        print("INVALID INPUT")

def s_showrecords():
    d1=pymysql.connect(host="localhost",user="root",passwd="root",database="hotel")
    #c1=d1.cursor()
    quer="select * from staff;"
    df=pd.read_sql(quer,d1)
    print(df)

def s_addrecords():
    d1=pymysql.connect(host="localhost",user="root",passwd="root",database="hotel")
    c1=d1.cursor()
    staffid = input("Guest id: ")
    name_of_staff = input("Name of staff: ")
    print("1. Managment \n2. Cleaning \n3. Food & Beverages")
    x=""
    dept = int(input("For Department select the no: "))
    if dept==1:
        x="Managment"
    elif dept==2:
        x="Cleaning"
    elif dept==3:
        x="Food & Beverages"    
    else:
        x="Dept not entered"
    sal = input("Salary: ")
    hiredate = input("Hire date: ")
    val = (staffid, name_of_staff, x, sal, hiredate)
    quer=("INSERT INTO staff(id, name, dept, sal, hiredate) VALUES(%s, %s, %s, %s, %s);") 
    print(c1.execute(quer, val))
    d1.commit()
    print("Record Added")

def s_search():
    d1=pymysql.connect(user="root",host="localhost",passwd="root",database="hotel")
    #c1=d1.cursor() 
    x=input("Staff id: ")
    quer="select * from staff where id=" +str(x)
    df=pd.read_sql(quer,d1)
    if df.size!=0:
        print(df)
    else:
        print("Staff ", x, "isn't present")

def s_delete():
    d1=pymysql.connect(host="localhost",user="root",passwd="root",database="hotel")
    c1=d1.cursor()   
    x=int(input("Enter the id:"))
    quer="delete from staff where id=%d;" %x
    rowcount=c1.execute(quer)
    if rowcount>0:
        d1.commit()
        print("Record Deleted")
    else:
        print("NO RECORD FOUND")

def s_graphics():
    d1=pymysql.connect(host="localhost",user="root",passwd="root",database="hotel")
    #c1=d1.cursor()
    print("1. Department \n2. Salary")
    x=int(input("enter the no: "))
    if x==1:
        deptgraph()
    elif x==2:
        salgraph()
    else:
        print("INVALID INPUT")

def deptgraph():
    d1=pymysql.connect(host="localhost",user="root",passwd="root",database="hotel")
    c1=d1.cursor()
    quer="select count(*) from staff where dept='Managment';"
    c1.execute(quer)
    x=c1.fetchone()
    lst=list(x)
    quer="select count(*) from staff where dept='Cleaning';"
    c1.execute(quer)
    y=c1.fetchone()
    lst1=list(y)
    quer="select count(*) from staff where dept='Food & Beverages';"
    c1.execute(quer)
    z=c1.fetchone()
    lst2=list(z)
    lstt=lst+lst1+lst2
    y=["Managment","Cleaning","Food & Beverages"]
    plt.bar(y,lstt)
    plt.xlabel("Department")
    plt.ylabel("No. of Staff")
    plt.title("Deptartment Graph")
    plt.show()

def salgraph():
    d1=pymysql.connect(host="localhost",user="root",passwd="root",database="hotel")
    c1=d1.cursor()
    quer="select count(*) from staff where sal<2000;"
    c1.execute(quer)
    x=c1.fetchone()
    xlst=list(x)
    quer="select count(*) from staff where sal between 2000 and 4000;"
    c1.execute(quer)
    x=c1.fetchone()
    lst=list(x)
    quer="select count(*) from staff where sal between 4000 and 6000;"
    c1.execute(quer)
    y=c1.fetchone()
    lst1=list(y)
    quer="select count(*) from staff where sal>6000;"
    c1.execute(quer)
    z=c1.fetchone()
    lst2=list(z)
    lstt=xlst+lst+lst1+lst2
    y=["Below 2000","2000 to 4000","4000 to 6000","Above 6000"]
    plt.bar(y,lstt)
    plt.xlabel("Salary")
    plt.ylabel("No. of Staff")
    plt.title("Staff Salary")
    plt.show() 
#needs to be fixed
def s_updaterecords():
    d1=pymysql.connect(user="root",host="localhost",passwd="root",database="hotel")
    c1=d1.cursor()
    gid=int(input("Enter the id of whomever you want to update the record of : "))
    quer="select * from staff where id=%d" % gid
    c1.execute(quer)
    if c1.rowcount>0:
        row=list(c1.fetchone())
        df=pd.read_sql(quer,d1)
        print(df)
        print("\n1. Name \n2. Deptartment \n3. Salary \n4. Hiredate")
        cr=int(input("Enter the no: "))

        #Name of staff
        if cr==1:
            y=input("Enter the new name of staff: ")
            quer="update staff set name='%s' where id=%d" %(y,gid)
            c1.execute(quer)
            d1.commit()
            print("Record Updated")
        #Dept             
        elif cr==2:
            print()
            print("1. Managment \n2. Cleaning \n3. Food & Beverages")
            x=""
            dept = int(input("For Department select the no: "))
            if dept==1:
                x="Managment"
            elif dept==2:
                x="Cleaning"
            elif dept==3:
                x="Food & Beverages"    
            else:
                x="Dept not entered"
            quer="update staff set dept='%s' where id=%d" %(x, gid)
            c1.execute(quer)
            d1.commit()
            print("Record Updated") 
        #Salary               
        elif cr==3:
            y=input("Enter the new Salary: ")
            quer="update staff set sal='%s' where id=%d" %(y,gid)
            c1.execute(quer)
            d1.commit()
            print("Record Updated")
        #Hiredate    
        elif cr==4:
            y=input("Enter the new hiredate in yyyy-mm-dd: ")
            quer="update staff set hiredate='%s' where id=%d" %(y,gid)
            c1.execute(quer)
            d1.commit()
            print("Record Updated")     
    elif c1.rowcount==0 or c1!=[1,2,3,4]:
        print("NO RECORD FOUND TO CHANGE")

print()
print("░█████╗░███╗░░██╗░█████╗░░█████╗░░██████╗░█████╗░")
print("██╔══██╗████╗░██║██╔══██╗██╔══██╗██╔════╝██╔══██╗")
print("███████║██╔██╗██║██║░░╚═╝███████║╚█████╗░███████║")
print("██╔══██║██║╚████║██║░░██╗██╔══██║░╚═══██╗██╔══██║")
print("██║░░██║██║░╚███║╚█████╔╝██║░░██║██████╔╝██║░░██║")
print("╚═╝░░╚═╝╚═╝░░╚══╝░╚════╝░╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝")
print()

print("1. Guest Records \n2. Staff Records \n3. Exit")
x = int(input("Enter the no. "))

if x==1:
    guest()
elif x==2:
    staff()
elif x==3:
        print()
        quit()
else:
    print()
    print("INVALID INPUT")
    print("exiting...")
    #even if quit() not used it'll auto exit
    #quit()

'''
SQL_QUERIES_FOR_HOTEL
CREATE TABLE guest (
	guestid int(11) NOT NULL,
	nameofguest varchar(50),
	type_of_room varchar(20),
	nofdays int(11),
	cidate date,
	codate date,
	room_no int(11),
	source_of_booking varchar(10),
	netpay int(11),
	PRIMARY KEY (guestid),
	UNIQUE (room_no)	
);

CREATE TABLE staff (
	id int(11) NOT NULL,
	name_of_staff varchar(50),
	dept varchar(20),
	sal int(11),
	hiredate date,
	PRIMARY KEY (id)
);
'''


   




