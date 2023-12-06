# app.py

from flask import Flask, request, render_template, redirect, flash, url_for, session
from models import User, Feedback, db, connect_db
from forms import RegisterForm, LoginForm, FeedbackForm, EditFeedbackForm
from werkzeug.routing import BaseConverter


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
        return redirect('/users/{username}')
    
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
            flash (f'Welcome back, {user.first_name} {user.last_name}!', 'success')
            session['username']=user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors=['Invalid name/password.']
        
    return render_template('login.html', form=form)

@app.route('/secret')
def secret():
    if 'username' not in session:
        flash ('Please login!', 'danger')
        return redirect('/login')       
    return render_template('secret.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')

@app.route('/users/<username>')
def user_info(username):
    if 'username' not in session:
        flash ('Please login!', 'danger')
        return redirect('/login')
    else:
        user=User.query.get_or_404(username)
        form=FeedbackForm()
        feedback=Feedback.query.filter_by(username=user.username).all()
        print(f"Feedback for {user.username}: {feedback}")
        return render_template('user_info.html', user=user, all_feedback=feedback, form=form) 
    
@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if 'username' not in session:
        flash('Please login', 'danger')
        return redirect('/login')
    user=User.query.get_or_404(username)
    feedback=Feedback.query.filter_by(username=user.username).all()
    for fb in feedback:
        db.session.delete(fb)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted', 'success')

    return redirect('/users/{username}/feedback/add')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if 'username' not in session:
        flash ('Please login!', 'danger')
        return redirect('/login')
    else:
        form=FeedbackForm()

        if form.validate_on_submit():
            title=form.title.data
            content=form.content.data
            new_feedback=Feedback(title=title, content=content, username=session['username'])
            db.session.add(new_feedback)
            db.session.commit()
            return redirect(url_for('user_info', username=username))

        return render_template('feedback.html', form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    if 'username' not in session:
        flash ('Please login!', 'danger')
        return redirect('/login')
    else:
        feedback=Feedback.query.get_or_404(feedback_id)
        form=EditFeedbackForm(obj=feedback)
        if form.validate_on_submit():
            feedback.title=form.title.data
            feedback.content=form.content.data
            db.session.commit()
            flash('Feedback updated successfully', 'success')
            return redirect(url_for('user_info', username=feedback.username))
        return render_template('edit_feedback.html', form=form, feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    if 'username' not in session:
        flash('Please login', 'danger')
        return redirect('/login')
    feedback=Feedback.query.get_or_404(feedback_id)
    if feedback.username==session['username']:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback deleted', 'success')
    else:
        flash('You do not have permission to do that!', 'danger')
    return redirect(url_for('user_info', username=feedback.username))
