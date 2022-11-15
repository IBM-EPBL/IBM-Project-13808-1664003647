from flask import Flask, render_template,request
# from flask_mysqldb import MYSQL

app = Flask(__name__)
# app.config['MYSQL_HOST']='localhost'
# app.config['MYSQL_USER']='root'
# app.config['MYSQL_PASSWORD']=''
# app.config['MYSQL_DATABASE']='flask'
# mysql = MYSQL(app)

@app.route('/')
def home_page():
    return render_template('home_page.html')

# @app.route('/registration')
# def registration():
#     return render_template('registration2.html')


@app.route('/score_Prediction')
def score_Prediction():
    return render_template('score_Prediction.html')

@app.route('/eligible')
def eligible():
    return render_template('eligible.html')


@app.route('/not_Eligible')
def not_Eligible():
    return render_template('not_Eligible.html')


if __name__ == "__main__":
    app.run()