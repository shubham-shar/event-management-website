import datetime
import os
from flask import Flask, render_template, request, redirect, jsonify, url_for, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, UserAccounts, UserProfiles, Teams, Lists, ListItems, Messages, TeamMembers, Events, Comments

app = Flask(__name__)

engine = create_engine('sqlite:///event_database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
Session = DBSession()

@app.route('/')
@app.route('/events/')
def mainPage():
    return render_template('main_page.html', logged=session.get('username'))

@app.route('/<event_type>/')
def eventList(event_type):
    events = Session.query(Events).filter_by(type=event_type).all()
    return render_template('event_list.html', events=events, event_type=event_type, logged=session.get('username'))

@app.route('/<int:event_id>/', methods=['GET', 'POST'])
def eventInfo(event_id):
    if request.method == 'POST':
        add_comment = Comments(comment=request.form['add_comment'], post_date=datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"), event_id=event_id, username=session.get('username'))
        Session.add(add_comment)
        Session.commit()
        return redirect(url_for('eventInfo', event_id=event_id))
    else:
        event = Session.query(Events).filter_by(id=event_id).one()
        comments = Session.query(Comments).filter_by(event_id=event_id).all()
        return render_template('event_info.html', event=event, comments=comments, logged=session.get('username'))
    
@app.route('/signup/', methods=['GET', 'POST'])
def signupPage():
    if request.method == 'POST':
        user = UserAccounts(username=request.form['username'], password=request.form['password'])
        Session.add(user)
        Session.commit()
        profile = UserProfiles(f_name=request.form['f_name'], l_name=request.form['l_name'], dob=request.form['dob'], mobile=request.form['mobile'], gender=request.form['gender'], rollno=request.form['rollno'], username=request.form['username'], email=request.form['email'])
        Session.add(profile)
        Session.commit()
        return redirect(url_for('mainPage'))
    else:
        return render_template('signup_page.html')
    
@app.route('/login/', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        users = Session.query(UserAccounts).all()
        for i in users:
            if username == i.username and password == i.password:
                session['username'] = i.username
                session['acc_type'] = i.acc_type
                return redirect(url_for('mainPage'))
            else:
                session['username'] = False
                session['acc_type'] = False
        return redirect(url_for('loginPage'))
    else:
        return render_template('login_page.html')
    
@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html', logged=session.get('username'))

@app.route('/post_event/', methods=['GET', 'POST'])
def postEvent():
    if request.method == 'POST':
        event = Events(title=request.form['title'], type=request.form['type'], starts=request.form['starts'], ends=request.form['ends'], description=request.form['description'], contact=request.form['contact'], club=request.form['club'], post_date=datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
        Session.add(event)
        Session.commit()
        return redirect(url_for('eventInfo', event_id=event.id))
    else:
        return render_template('post_event.html')

#@app.route('/my_events/')
#def myEvents():
#    events = Session.query(Events).all()
#    return render_template('my_events.html', events=events)
    
#@app.route('/post_list/', methods=['GET', 'POST'])
#def postList():
#    if request.method == 'POST':

@app.route('/logout/')
def logout():
    session['username'] = None
    session['acc_type'] = None
    return redirect(url_for('mainPage'))

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
