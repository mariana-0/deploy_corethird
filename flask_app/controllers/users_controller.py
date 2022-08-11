from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt   

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validation(request.form):
        return redirect('/')
    
    pwd = bcrypt.generate_password_hash(request.form['password'])
    
    form = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pwd,
        'language':request.form['language'],
        'birth_date':request.form['birth_date']
    }
    
    id=User.create_user(form)
    session['id']=id
    
    return redirect('/success')

@app.route('/login', methods=['POST'])
def login():
    user = User.user_by_email(request.form)
    if not user: 
        flash('Wrong email', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Wrong password', 'login')
        return redirect('/')
    session['id']=user.id
    return redirect('/success')

@app.route('/success')
def success():
    if not 'id' in session:
        return redirect('/')
    data = {
        'id': session['id']
    }
    user = User.user_by_id(data)
    return render_template('success.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

