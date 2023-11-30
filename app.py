# app.py

from flask import Flask, request, render_template, redirect, flash, url_for, session
from models import User, Feedback, db, connect_db
from forms import RegisterForm, LoginForm, FeedbackForm


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "chickenzarecool21837"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

app.app_context().push()

@app.route('/')
def redirect_to_register():
    '''Redirect to /register.'''
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data
        first_name=form.first_name.data
        last_name=form.last_name.data

        new_user=User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()

        session['username']=new_user.username
        return redirect('/secret')
    
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()

    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data

        user=User.authenticate(username, password)

        if user:
            flash (f'Welcome back, {user.first_name} {user.last_name}!')
            session['username']=user.username
            return redirect('/secret')
        else:
            form.username.errors=['Invalid name/password.']
        
    return render_template('login.html', form=form)

@app.route('/secret')
def secret():
    return render_template('secret.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

@app.route('/users/<username>')
def user_info(username):
    if 'username' not in session:
        flash ('Please login!')
        return redirect('/login')
    else:
        user=User.query.get_or_404(username)
        return render_template('user_info.html', user=user) 
    
# @app.route('/users/<username>/delete', methods=['POST'])

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if 'username' not in session:
        flash ('Please login!')
        return redirect('/login')
    else:
        form=FeedbackForm()
        user=User.query.get_or_404(username)
        if form.validate_on_submit():
            title=form.title.data
            content=form.content.data
            return redirect('/users/<username>')
        else:
            return render_template('feedback.html', user=user)


# @app.route('/users/<int:feedback-id>/update', methods=['GET', 'POST'])

# @app.route('/users/<int:feedback-id>/delete', methods=['POST'])