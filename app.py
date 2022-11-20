from flask import Flask, render_template, redirect, flash, session
from models import db, connect_db,User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterUser, LoginUser, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.debug=True

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    """redirects to register"""
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def registration():
    """shows registration form and handles form to register users"""
    form = RegisterUser()
    if form.validate_on_submit():
        username = form.username.data
        u = User.query.filter_by(username=username).first()
        if u:
            flash('Username in Use')
            return render_template('register_form.html', form = form)
        password = form.password.data
        email= form.email.data
        first_name = form.first_name.data
        last_name= form.last_name.data
        user = User.register(username=username,pwd=password,email=email,first_name=first_name,last_name=last_name)
        db.session.add(user)
        db.session.commit()
        session['user_username'] = user.username
        return redirect (f'/user/{username}')
    return render_template('register_form.html', form = form)

@app.route('/login', methods=['GET','POST'])
def login():
    """shows login form and handles form to login users"""
    form = LoginUser()
    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        user = User.authenticate(username=username, pwd = pwd)
        if user:
            session['user_username'] = user.username
            return redirect(f'/user/{username}')
        else:
            flash('Incorrect username/password')
            return render_template('login_form.html', form=form)
    return render_template('login_form.html', form = form)

@app.route('/logout')
def logout():
    """logs users out"""
    session.pop('user_username')
    return redirect('/')

@app.route('/user/<username>')
def show_user(username):
    if 'user_username' in session:
        user = User.query.filter_by(username=username).first()
        if user:
            feedbacks = Feedback.query.filter(Feedback.username==username)
            return render_template('user.html', user = user, feedbacks = feedbacks, current_user=session['user_username'])
        else:
            flash('Could not find user')
            current_user = session['user_username']
            return redirect(f'/user/{current_user}')
    else:
        flash('Must be logged in')
        return redirect('/')

@app.route('/user/<username>/delete', methods=['POST'])
def delete_user(username):
    if session['user_username']==username:
        user = User.query.filter_by(username=username).delete()
        db.session.commit()
        session.pop('user_username')
        return redirect('/')
    elif 'user_username' in session:
        flash('Can not delete other users')
        current_user = session['user_username']
        return redirect(f'/user/{current_user}')
    else:
        flash('Must be logged in')
        return redirect('/')


@app.route('/user/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    if session['user_username']==username:
        form = FeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feedback = Feedback(title=title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f'/user/{username}')
        return render_template('add_feedback.html', form=form)
    elif 'user_username' in session:
        flash('Can not delete other users')
        current_user = session['user_username']
        return redirect(f'/user/{current_user}')
    else:
        flash('Must be logged in')
        return redirect('/')

@app.route('/feedback/<feedback_id>/update', methods=['GET','POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.filter_by(id=feedback_id).first()
    if session['user_username']==feedback.username:
        form = FeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feedback.title =title
            feedback.content=content
            db.session.commit()
            return redirect(f'/user/{feedback.username}')
        return render_template('update_feedback.html', form=form, feedback = feedback)
    elif 'user_username' in session:
        flash("Can not update other users' feedback")
        current_user = session['user_username']
        return redirect(f'/user/{current_user}')
    else:
        flash('Must be logged in')
        return redirect('/')

@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.filter_by(id=feedback_id).first()
    username = feedback.username
    if session['user_username']==username:
        feedback = Feedback.query.filter_by(id=feedback_id).delete()
        db.session.commit()
        return redirect(f'/user/{username}')
    elif 'user_username' in session:
        flash("Can not update other users' feedback")
        current_user = session['user_username']
        return redirect(f'/user/{current_user}')
    else:
        flash('Must be logged in')
        return redirect('/')