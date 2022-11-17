from flask import Flask, render_template,flash,redirect,url_for,session,request
import sqlite3
import requests

app = Flask(__name__)
app.secret_key="123"

con=sqlite3.connect("database.db")
con.execute("create table if not exists students(pid integer primary key,name text,email text,mobile integer,password text)")
con.close()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login',methods=["GET","POST"])
def index1():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from students where email=? and password=?",(email,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["name"]
            session["email"]=data["email"]
            session["password"]=data["password"]
            return redirect(url_for("home"))
        else:
            flash("Username and Password Mismatch","danger")
    return redirect(url_for("login"))


@app.route('/home',methods=["GET","POST"])
def home():
    return render_template("home.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            email=request.form['email']
            mobile=request.form['mobile']
            password=request.form['password']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("insert into students(name,email,mobile,password)values(?,?,?,?)",(name,email,mobile,password))
            con.commit()
            flash("Record Added  Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("login"))
            con.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/index", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        arr = []
        for i in request.form:
            val = request.form[i]
            if val == '':
                return redirect(url_for("predictor"))
            arr.append(float(val))

        # deepcode ignore HardcodedNonCryptoSecret: <please specify a reason of ignoring this>
        API_KEY = "wf8mge_OQdwVO8ao2kmWCtfxOfLWl8442SH44V85v2Ls"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
            "apikey": API_KEY, 
            "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
            })
        mltoken = token_response.json()["access_token"]
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
        payload_scoring = {
            "input_data": [{"fields":[  'GRE Score',
                                        'TOEFL Score',
                                        'University Rating',
                                        'SOP',
                                        'LOR ',
                                        'CGPA',
                                        'Research'], 
                            "values": [arr]
                            }]
                        }

        response_scoring = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/8308fd4c-24a5-46ab-96fa-263657ae4ad0/predictions?version=2022-10-18', 
            json=payload_scoring,
            headers=header
        ).json()
        
        result = response_scoring['predictions'][0]['values']
        
        if result[0][0] > 0.5:
            return redirect(url_for('eligible', percent=result[0][0]*100))
        else:
            return redirect(url_for('notEligible', percent=result[0][0]*100))
    else:
        return redirect(url_for("predictor"))

@app.route("/predictor")
def predictor():
    return render_template("predictor.html")

@app.route("/eligible/<percent>")
def eligible(percent):
    return render_template("eligible.html", content=[percent])

@app.route("/notEligible/<percent>")
def notEligible(percent):
    return render_template("notEligible.html", content=[percent])

@app.route('/<path:path>')

def catch_all():
    return redirect(url_for("predictor"))

if __name__ == '__main__':
    app.run(debug=True)
