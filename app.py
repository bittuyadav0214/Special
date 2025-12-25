from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from flask import session
from flask import url_for
from flask import redirect
import os
from datetime import datetime
from zoneinfo import ZoneInfo


ist_time = datetime.now(ZoneInfo("Asia/Kolkata"))


app = Flask(__name__)
app.secret_key="FLASKKESECRETBAA"

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route("/birthday",methods=["GET","POST"])
def birthday():
    if "heart" in session:
        if request.method == "POST":
            return "data received"  
        return render_template('birthday.html')   
    return redirect("/")

@app.route('/datalog',methods=["GET","POST"])
def log():
    if request.method=="POST":
        data = request.form.get("data")
        if data:
             with open("log/whoami.txt","a") as file:
                 file.write(f"{ist_time} ==> {data}\n")
                 file.close()
                 return "Successfully logged"
        return "Invalid data"
        
    return "send data in post"
    
@app.route('/verification',methods=["GET","POST"])
def verification():
    if request.method == "POST":
        name = request.form.get('name').lower()
        with open('log/user.txt','a') as file:
            file.write(f"{ist_time} ==> {name}\n")
            file.close()
        if name.strip() == "nandani" or name.strip() == "suhani":
            session['heart'] = name
            return redirect(url_for('birthday'))
        else:
            return render_template('auth.html',status="style=display:block")
    return render_template('auth.html')
    
@app.route('/logdata',methods=["GET","POST"])
def viewlog():
    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        if username == "bittuyadav" and password == "bittuyadav0214" :
            with open("log/user.txt","r") as userlogfile:
                userlog = userlogfile.readlines()
                userlogfile.close()
            with open("log/whoami.txt","r") as whoamifile:
                whoamilog = whoamifile.readlines()
                whoamifile.close()
            return Response(f'<h1>Users Log </h1><br><br>{userlog}<br><br><h1>Whoami Log</h1><br><br>{whoamilog}')
        return Response("<h1><strong>[^°^ Invalid Credentials ^°^]</strong></h1>")  
    return render_template('logauth.html')                 
@app.errorhandler(404)
def not_found(error):
    return redirect('/')    

if __name__ == "__main__":
    app.run()
