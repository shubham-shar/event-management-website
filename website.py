import datetime
import os
from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, UserAccounts, UserProfiles, Teams, ListItems
from database_setup import Messages, TeamMembers, Events, Comments, TeamMessages

app = Flask(__name__)

engine = create_engine('sqlite:///event_database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
Session = DBSession()

###############################################################################

@app.route('/')
@app.route('/events/')
def mainPage():
    return render_template('display/main_page.html',
                           logged=session.get('username'))

###############################################################################

@app.route('/<event_type>/')
def eventList(event_type):
    events = Session.query(Events).filter_by(type=event_type).all()
    return render_template('display/event_list.html', events=events,
                           event_type=event_type,
                           logged=session.get('username'))

###############################################################################

@app.route('/<int:event_id>/', methods=['GET', 'POST'])
def eventInfo(event_id):
    if request.method == 'POST':
        if session.get('username') == None:
            return redirect(url_for('loginPage'))
        else:
            add_comment = Comments(comment=request.form['add_comment'],
                                   post_date=datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                                   event_id=event_id,
                                   username=session.get('username'))
            Session.add(add_comment)
            Session.commit()
            return redirect(url_for('eventInfo', event_id=event_id))
    else:
        event = Session.query(Events).filter_by(id=event_id).one()
        comments = Session.query(Comments).filter_by(event_id=event_id).all()
        return render_template('display/event_info.html', event=event,
                               comments=comments,
                               logged=session.get('username'))
    
###############################################################################

@app.route('/<int:comment_id>/delete_comment/')
def deleteComment(comment_id):
    if session.get('username') != None:
        comment = Session.query(Comments).filter_by(id=comment_id).one()
        event_id = comment.event_id
        if session.get('username') == comment.username or session.get('acc_type') == 'master':
            Session.delete(comment)
            Session.commit()
        return redirect(url_for('eventInfo', event_id=event_id))
    else:
        return redirect(url_for('error'))

###############################################################################
    
@app.route('/signup/', methods=['GET', 'POST'])
def signupPage():
    if session.get('username') == None:
        if request.method == 'POST':
            user = UserAccounts(username=request.form['username'],
                                password=request.form['password'])
            Session.add(user)
            Session.commit()
            profile = UserProfiles(f_name=request.form['f_name'],
                                   l_name=request.form['l_name'],
                                   dob=request.form['dob'],
                                   mobile=request.form['mobile'],
                                   gender=request.form['gender'],
                                   rollno=request.form['rollno'],
                                   username=request.form['username'],
                                   email=request.form['email'])
            Session.add(profile)
            Session.commit()
            return redirect(url_for('mainPage'))
        else:
            return render_template('display/signup_page.html')
    else:
        return redirect(url_for('error'))
    
###############################################################################
    
@app.route('/login/', methods=['GET', 'POST'])
def loginPage():
    if session.get('username') == None:
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
                    session['username'] = None
                    session['acc_type'] = None
            return redirect(url_for('loginPage'))
        else:
            return render_template('display/login_page.html')
    else:
        return redirect(url_for('error'))
    
###############################################################################
    
@app.route('/logout/')
def logout():
    if session.get('username') != None:
        session['username'] = None
        session['acc_type'] = None
        return redirect(url_for('mainPage'))
    else:
        return redirect(url_for('error'))

###############################################################################

@app.route('/dashboard/')
def dashboard():
    if session.get('username') != None:
        return render_template('dashboard/dashboard.html',
                               logged=session.get('username'),
                               acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('error'))
    
###############################################################################

@app.route('/post_event/', methods=['GET', 'POST'])
def postEvent():
    if session.get('username') != None:
        if request.method == 'POST':
            event = Events(title=request.form['title'],
                           type=request.form['type'],
                           starts=request.form['starts'],
                           ends=request.form['ends'],
                           description=request.form['description'],
                           contact=request.form['contact'],
                           club=request.form['club'],
                           post_date=datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                           head=request.form['head'])
            user = Session.query(UserAccounts).filter_by(username=event.head).one()
            if not user.acc_type == 'master':
                user.acc_type='event_head'
            Session.add(event)
            Session.add(user)
            Session.commit()
            return redirect(url_for('eventInfo', event_id=event.id))
        else:
            users = Session.query(UserAccounts).all()
            return render_template('dashboard/post_event.html',
                                   logged=session.get('username'), users=users,
                                   acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('error'))
    
###############################################################################
    
@app.route('/permission/', methods=['GET', 'POST'])
def permission():
    if session.get('username') != None:
        if request.method == 'POST':
            user = Session.query(UserAccounts).filter_by(username=request.form['username']).one()
            user.acc_type = "default"
            Session.add(user)
            Session.commit()
            return redirect(url_for('permission'))
        else:
            users = Session.query(UserAccounts).all()
            return render_template('dashboard/permission.html',
                                   users=users, logged=session.get('username'),
                                   acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('error'))

###############################################################################

@app.route('/edit_profile/', methods=['GET', 'POST'])
def editProfile():
    if session.get('username') != None:
        profile = Session.query(UserProfiles).filter_by(username=session.get('username')).one()
        if request.method == 'POST':
            profile.f_name=request.form['f_name']
            profile.l_name=request.form['l_name']
            profile.dob=request.form['dob']
            profile.mobile=request.form['mobile']
            profile.gender=request.form['gender']
            profile.rollno=request.form['rollno']
            profile.email=request.form['email']
            Session.add(profile)
            Session.commit()
            return redirect(url_for('editProfile'))
        else:
            return render_template('dashboard/edit_profile.html',
                                   logged=session.get('username'),
                                   profile=profile,
                                   acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('error'))
    
###############################################################################
    
@app.route('/manage_events/')
def manageEvents():
    if session.get('username') != None:
        events = Session.query(Events).filter_by(head=session.get('username')).all()
        return render_template('dashboard/manage_events.html', events=events,
                               logged=session.get('username'),
                               acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('error'))
    
###############################################################################

@app.route('/<int:event_id>/create_team/', methods=['GET', 'POST'])
def createTeam(event_id):
    if session.get('username') != None:
        if request.method == 'POST':
            team_head = Session.query(UserAccounts).filter_by(username=request.form['team_head']).one()
            team_head.acc_type = 'teamhead'
            team = Teams(name=request.form['name'],
                         team_head=request.form['team_head'],
                         event_id=event_id)
            Session.add(team_head)
            Session.add(team)
            Session.commit()
            return redirect(url_for('createTeam', event_id=event_id))
        else:
            event = Session.query(Events).filter_by(id=event_id).one()
            users = Session.query(UserAccounts).all()
            return render_template('dashboard/create_team.html',
                                   logged=session.get('username'), users=users,
                                   event=event,
                                   acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('error'))
    
###############################################################################

@app.route('/<int:event_id>/event_options/')
def eventOptions(event_id):
    if session.get('username') != None:
        event = Session.query(Events).filter_by(id=event_id).one()
        return render_template('dashboard/event_options.html',
                               logged=session.get('username'), event=event,
                               acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('error'))

###############################################################################

@app.route('/<int:event_id>/delete_event/')
def deleteEvent(event_id):
    if session.get('username') != None:
        event = Session.query(Events).filter_by(id=event_id).one()
        Session.delete(event)
        Session.commit()
        return redirect(url_for('manageEvents'))
    else:
        return redirect(url_for('error'))

###############################################################################

@app.route('/<int:event_id>/edit_event/', methods=['GET', 'POST'])
def editEvent(event_id):
    if session.get('username') != None:
        event = Session.query(Events).filter_by(id=event_id).one()
        if request.method == 'POST':
            event.title=request.form['title']
            event.type=request.form['type']
            event.starts=request.form['starts']
            event.ends=request.form['ends']
            event.description=request.form['description']
            event.contact=request.form['contact']
            event.club=request.form['club']
            Session.add(event)
            Session.commit()
            return redirect(url_for('eventOptions', event_id=event_id))
        else:
            return render_template('dashboard/edit_event.html',
                                   logged=session.get('username'),
                                   event=event,
                                   acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('error'))
    
###############################################################################

@app.route('/send_message/', methods=['GET', 'POST'])
def sendMessage():
    if session.get('username') != None:
        if request.method == 'POST':
            message = Messages(title=request.form['title'],
                               message=request.form['message'],
                               time=datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                               from_user=session.get('username'),
                               username=request.form['username'])
            Session.add(message)
            Session.commit()
            return redirect(url_for('sendMessage'))
        else:
            users = Session.query(UserAccounts).filter_by(acc_type='master').all()
            return render_template('dashboard/message.html',
                                   logged=session.get('username'), users=users,
                                   acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('error'))

###############################################################################

@app.route('/inbox/')
def inbox():
    if session.get('username') != None:
        messages = Session.query(Messages).filter_by(username=session.get('username')).all()
        return render_template('dashboard/inbox.html',
                               logged=session.get('username'),
                               messages=messages,
                               acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('error'))

###############################################################################

@app.route('/error/')
def error():
    return render_template('error.html')

###############################################################################

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
