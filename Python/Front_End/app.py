from flask import Flask, request, render_template

import sqlite3

app=Flask(__name__)
firstNameLP=''
lastNameLP=''
try:
	conn=sqlite3.connect('Employee.db',isolation_level=None)
	c = conn.cursor()	
	c.execute('CREATE TABLE IF NOT EXISTS info(id INTEGER PRIMARY KEY, last TEXT, first TEXT, middle TEXT, dob TEXT,social TEXT, hire TEXT, gend TEXT)')
	c.execute('CREATE TABLE IF NOT EXISTS conta(id INTEGER PRIMARY KEY, last TEXT, first TEXT, middle TEXT, email TEXT, phone TEXT,street TEXT, zip TEXT, state TEXT, country TEXT)')
	c.execute('CREATE TABLE IF NOT EXISTS sal(id INTEGER PRIMARY KEY, last TEXT, first TEXT, middle TEXT, year TEXT, hour TEXT, week TEXT, qua TEXT, fromDa TEXT, toDa TEXT, ot TEXT)')
	c.execute('CREATE TABLE IF NOT EXISTS dept(id INTEGER PRIMARY KEY, last TEXT, first TEXT, middle TEXT,dnum TEXT, dname TEXT, title TEXT)')
	c.execute('CREATE TABLE IF NOT EXISTS passW(password TEXT)')
	c.execute('SELECT * FROM passW')
	if len(c.fetchall())==0:
		c.execute("INSERT INTO passW VALUES('18016A3269')")
		
	conn.commit()
except Exception as e:
	print e
	
#Web Pages----------------------------
@app.route('/')
def index():
	return render_template('home.html')

	
@app.route('/view', methods=['POST'])	
def view():
	c.execute('SELECT * FROM info')
	data=c.fetchall()
	c.execute('SELECT * FROM conta')
	contact=c.fetchall()
	c.execute('SELECT * FROM dept')
	depart=c.fetchall()
	c.execute('SELECT * FROM sal')
	sala=c.fetchall()
	conn.commit()
	return render_template('view.html',data=data,contact=contact,salaries=sala,depart=depart)

	
@app.route('/delete', methods=['POST'])	
def delete():
	return render_template('delete.html',mess=0)
	
@app.route('/edit', methods=['POST'])	
def edit():
	return render_template('edit.html',mess=0,choice=0)
	
@app.route('/backMain')	
def backMain():
	return render_template('new.html')
	
	
@app.route('/update', methods=['POST'])	
def update():
	return render_template('update.html',mess=0)
	
	
@app.route('/search', methods=['POST'])	
def search():
	return render_template('search.html',mess=0,filling=0)
	
	
@app.route('/delFINAL', methods=['POST'])	
def delFINAL():
	c.execute('SELECT * FROM passW LIMIT 1')
	passGood=c.fetchone()
	if request.form['commandD']==passGood[0]:
		c.execute('DELETE FROM info')
		c.execute('DELETE FROM conta')
		c.execute('DELETE FROM dept')
		c.execute('DELETE FROM sal')
		conn.commit()
		return render_template('delete.html',mess=1,message="Database has been cleared!")
	else:
		return render_template('delete.html',mess=1,message="Password Incorrect!")

#Web Pages END-----------------------------------

#Login
@app.route('/echo', methods=['POST'])
def echo():
	password=request.form['pass']
	c.execute('SELECT * FROM passW LIMIT 1')
	goodPass=c.fetchone()
	conn.commit()
	if password==goodPass[0]:
		return render_template('new.html',mess=0)
	else:
		return render_template('home.html')
		
@app.route('/fileSend', methods=['POST'])
def fileSend():
	try:
		input=request.form['outputs']
		input=input.split("\n")
		FIR=input[1].strip()
		LAS=input[0].strip()
		c.execute('SELECT * FROM info')
		emp=len(c.fetchall())+1
		c.execute('INSERT INTO info (id, last, first, middle, dob, social, hire, gend) VALUES (?,?,?,?,?,?,?,?)',
			(emp,LAS,FIR,input[2].strip(),input[3].strip(),input[4].strip(),input[5].strip(),input[6].strip()))
		c.execute('INSERT INTO conta (id, last, first, middle,email,phone,street,zip,state,country) VALUES (?,?,?,?,?,?,?,?,?,?)',	
			(emp,LAS,FIR,input[2].strip(),input[7].strip(),input[8].strip(),input[9].strip(),input[10].strip(),input[11].strip(),input[12].strip()))
		c.execute('INSERT INTO sal (id, last, first, middle, year, hour, week, qua, fromDa, toDa, ot) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
			(emp,LAS,FIR,input[2].strip(),input[13].strip(),input[14].strip(),input[15].strip(),input[16].strip(),input[17].strip(),input[18].strip(),input[19].strip()))
		c.execute('INSERT INTO dept (id, last, first, middle, dnum, dname, title ) VALUES (?,?,?,?,?,?,?)',
			(emp,LAS,FIR,input[2].strip(),input[20].strip(),input[21].strip(),input[22].strip()))
		conn.commit()
		messs=FIR+" "+LAS+" has been successfully added!"
		return render_template('update.html', mess=1,message=messs)
	except Exception as e:
		print e
		
@app.route('/searchWord', methods=['POST'])
def searchWord():
	TTT=request.form['word']
	term='%'+request.form['word']+'%'
	ind=0
	allInf=[]
	allCon=[]
	allSal=[]
	allDep=[]
	
	countersI=[]
	countersC=[]
	countersS=[]
	countersD=[]
	c.execute('SELECT * FROM info')
	emp=len(c.fetchall())+1
	st=0
	while st<emp:
		countersI.append(1)
		countersC.append(1)
		countersS.append(1)
		countersD.append(1)
		st+=1
	elInfo=['last','first','middle','dob','social','hire','gend',     'last','first','middle','email','phone','street','zip','state','country',    'last','first','middle','year','hour','week','qua','fromDa','toDa','ot',   'last','first','middle','dnum','dname','title'];
		
	for col in elInfo:
		if ind<7:
			c.execute('SELECT * FROM info WHERE '+col+' LIKE ?',(term,))
			hold=c.fetchall()
			for entry in hold:
				countersI[entry[0]]-=1
				if countersI[entry[0]]>-1:
					allInf.append(list(entry))
				
		elif ind<16:
			c.execute('SELECT * FROM conta WHERE '+col+' LIKE ?',(term,))
			hold=c.fetchall()
			for entry in hold:
				countersC[entry[0]]-=1
				if countersC[entry[0]]>-1:
					allCon.append(list(entry))
		elif ind<26:
			c.execute('SELECT * FROM sal WHERE '+col+' LIKE ?',(term,))
			hold=c.fetchall()
			for entry in hold:
				countersS[entry[0]]-=1
				if countersS[entry[0]]>-1:
					allSal.append(list(entry))		
		else:
			c.execute('SELECT * FROM dept WHERE '+col+' LIKE ?',(term,))
			hold=c.fetchall()
			for entry in hold:
				countersD[entry[0]]-=1
				if countersD[entry[0]]>-1:
					allDep.append(list(entry))
		ind+=1
	return render_template('search.html',mess=0,filling=1,aInf=allInf,aCon=allCon,aSal=allSal,aDep=allDep,termW=TTT)
		
				
@app.route('/updatePASS', methods=['POST'])
def updatePASS():
	newP=request.form['newP']
	trial=request.form['oldP']
	c.execute('SELECT * FROM passW LIMIT 1')
	goodPass=c.fetchone()
	if trial==goodPass[0]:
		c.execute('DELETE FROM passW')
		c.execute('INSERT INTO passW(password) VALUES (?)',(newP,))
		conn.commit()
		return render_template('new.html',mess=1,message='Password Updated!')
	else:
		return render_template('new.html',mess=1,message='Password Incorrect!')
		
		
@app.route('/rem',methods=['POST'])
def rem():
	try:
		conn.commit()
		nameFI=request.form['FI']
		nameLA=request.form['LA']
		c.execute('SELECT * FROM info WHERE first=? AND last=?', (nameFI,nameLA))
		num=c.fetchone()
		indexO=num[0]
		c.execute('DELETE FROM info WHERE first=? AND last=?', (nameFI,nameLA))
		c.execute('DELETE FROM conta WHERE first=? AND last=?', (nameFI,nameLA))
		c.execute('DELETE FROM dept WHERE first=? AND last=?', (nameFI,nameLA))
		c.execute('DELETE FROM sal WHERE first=? AND last=?', (nameFI,nameLA))
		c.execute('UPDATE info SET id=id-1 WHERE id>?',(indexO,))
		c.execute('UPDATE conta SET id=id-1 WHERE id>?',(indexO,))
		c.execute('UPDATE dept SET id=id-1 WHERE id>?',(indexO,))
		c.execute('UPDATE sal SET id=id-1 WHERE id>?',(indexO,))
		conn.commit()
		return render_template('update.html',mess=1,message=nameFI+" "+nameLA+" has been removed successfully.")
	except Exception as e:
		return render_template('update.html',mess=1,message="Employee cannot be found!")

@app.route('/SEL',methods=['POST'])
def SEL():
	try:
		nameFI=request.form['FI']
		nameLA=request.form['LA']
		global firstNameLP
		firstNameLP=nameFI
		global lastNameLP
		lastNameLP=nameLA
		c.execute('SELECT * FROM info WHERE first=? AND last=?', (nameFI,nameLA))
		inform=c.fetchone()
		c.execute('SELECT * FROM conta WHERE first=? AND last=?', (nameFI,nameLA))
		contac=c.fetchone()
		c.execute('SELECT * FROM dept WHERE first=? AND last=?', (nameFI,nameLA))
		depart=c.fetchone()
		c.execute('SELECT * FROM sal WHERE first=? AND last=?', (nameFI,nameLA))
		salar=c.fetchone()
		return render_template('edit.html',mess=1,message='Loaded Successfully!',choice=1,Info=inform,Contact=contac,Department=depart,Salary=salar)
	except Exception as e:
		print e
		return render_template('edit.html',mess=1,message='Employee not found!',choice=0)
			

@app.route('/editCommit', methods=['POST'])	
def editCommit():
	try:
		nameF=request.form['nameF']
		nameL=request.form['nameL']
		nameM=request.form['nameM']
		dob=request.form['dob']
		socS=request.form['ss']
		hireD=request.form['hireD']
		gend=request.form['gend']
		email=request.form['email']
		phone=request.form['phone']
		street=request.form['street']
		zip=request.form['zip']
		state=request.form['state']
		country=request.form['country']
		annS=request.form['annS']
		hourS=request.form['hourS']
		weekS=request.form['weekS']
		qSal=request.form['qSal']
		fromD=request.form['fromD']
		toD=request.form['toD']
		overT=request.form['overT']
		deptN=request.form['deptN']
		deptName=request.form['deptName']
		title=request.form['title']
		c.execute('SELECT * FROM info')
		emp=len(c.fetchall())+1
		c.execute('UPDATE info SET last=?, first=?, middle=?, dob=?, social=?, hire=?, gend=? WHERE first=? AND last=?',
			(nameL,nameF,nameM,dob,socS,hireD,gend,firstNameLP,lastNameLP))
		c.execute('UPDATE conta SET last=?, first=?, middle=?,email=?,phone=?,street=?,zip=?,state=?,country=? WHERE first=? AND last=?',
			(nameL,nameF,nameM,email,phone,street,zip,state,country,firstNameLP,lastNameLP))
		c.execute('UPDATE sal SET last=?, first=?, middle=?, year=?, hour=?, week=?, qua=?, fromDa=?, toDa=?, ot=? WHERE first=? AND last=?',
			(nameL,nameF,nameM,annS,hourS,weekS,qSal,fromD,toD,overT,firstNameLP,lastNameLP))
		c.execute('UPDATE dept SET last=?, first=?, middle=?, dnum=?, dname=?, title=? WHERE first=? AND last=?',
			(nameL,nameF,nameM,deptN,deptName,title,firstNameLP,lastNameLP))
		conn.commit()
		return render_template('edit.html',mess=1,message='Updated Successfully!',choice=0)
	except Exception as e:
		print e	

		
@app.route('/added', methods=['POST'])	
def added():
	try:
		nameF=request.form['nameF']
		nameL=request.form['nameL']
		nameM=request.form['nameM']
		dob=request.form['dob']
		socS=request.form['ss']
		hireD=request.form['hireD']
		gend=request.form['gend']
		email=request.form['email']
		phone=request.form['phone']
		street=request.form['street']
		zip=request.form['zip']
		state=request.form['state']
		country=request.form['country']
		annS=request.form['annS']
		hourS=request.form['hourS']
		weekS=request.form['weekS']
		qSal=request.form['qSal']
		fromD=request.form['fromD']
		toD=request.form['toD']
		overT=request.form['overT']
		deptN=request.form['deptN']
		deptName=request.form['deptName']
		title=request.form['title']
		c.execute('SELECT * FROM info')
		emp=len(c.fetchall())+1
		c.execute('INSERT INTO info (id, first, last, middle, dob, social, hire, gend) VALUES (?,?,?,?,?,?,?,?)',
			(emp,nameF,nameL,nameM,dob,socS,hireD,gend))
		c.execute('INSERT INTO conta (id, first, last, middle,email,phone,street,zip,state,country) VALUES (?,?,?,?,?,?,?,?,?,?)',
			(emp,nameF,nameL,nameM,email,phone,street,zip,state,country))
		c.execute('INSERT INTO sal (id, first, last, middle, year, hour, week, qua, fromDa, toDa, ot) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
			(emp,nameF,nameL,nameM,annS,hourS,weekS,qSal,fromD,toD,overT))
		c.execute('INSERT INTO dept (id, first, last, middle, dnum, dname, title ) VALUES (?,?,?,?,?,?,?)',
			(emp,nameF,nameL,nameM,deptN,deptName,title))
		conn.commit()
		return render_template('update.html', mess=1,message=nameF+" "+nameL+" has been successfully added!")
	except Exception as e:
		print e
	
if __name__=='__main__':
	app.run()