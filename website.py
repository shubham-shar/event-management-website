import datetime
import os
import re
from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, UserAccounts, UserProfiles, Teams, ListItems
from database_setup import Messages, TeamMembers, Events, Comments, TeamMessages

app = Flask(__name__)

engine = create_engine('sqlite:///event_database.sql')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
Session = DBSession()

USER_RE = re.compile(r"^(?![-._])(?!.*[_.-]{2})[\w.-]{6,30}(?<![-._])$")


def valid_username(username):
    return username and USER_RE.match(username)


PASS_RE = re.compile(r"^.{3,20}$")


def valid_password(password):
    return password and PASS_RE.match(password)


@app.route('/')
@app.route('/events/')
def mainPage():
    return render_template('display/main_page.html',
                           logged=session.get('username'))


@app.route('/<event_type>/')
def eventList(event_type):
    events = Session.query(Events).filter_by(type=event_type).all()
    events.reverse()
    for event in events:
        print type(event)
    return render_template('display/event_list.html', events=events,
                           event_type=event_type,
                           logged=session.get('username'))


@app.route('/<int:event_id>/', methods=['GET', 'POST'])
def eventInfo(event_id):
    if request.method == 'POST':
        if session.get('username') is None:
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
        head = Session.query(UserProfiles).filter_by(username=event.head).one()
        return render_template('display/event_info.html', event=event,
                               comments=comments, head=head,
                               logged=session.get('username'))


@app.route('/<int:comment_id>/delete_comment/')
def deleteComment(comment_id):
    if session.get('username') is not None:
        comment = Session.query(Comments).filter_by(id=comment_id).one()
        event_id = comment.event_id
        if session.get('username') == comment.username or session.get('acc_type') == 'master':
            Session.delete(comment)
            Session.commit()
        return redirect(url_for('eventInfo', event_id=event_id))
    else:
        return redirect(url_for('not_found'))


@app.route('/signup/', methods=['GET', 'POST'])
def signupPage():
    if session.get('username') is None:
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
        return redirect(url_for('not_found'))


@app.route('/change_password/', methods=['GET', 'POST'])
def changePassword():
    if session.get('username') is not None:
        if request.method == 'POST':
            user = Session.query(UserAccounts).filter_by(
                username=session.get('username')).one()
            if user.password == request.form['oldpassword'] and valid_password(request.form['newpassword']):
                user.password = request.form['newpassword']
                Session.add(user)
                Session.commit()
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('not_found'))
        else:
            return render_template('dashboard/change_password.html',
                                   logged=session.get('username'),
                                   acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('not_found'))


@app.route('/login/', methods=['GET', 'POST'])
def loginPage():
    if session.get('username') is None:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
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
        return redirect(url_for('not_found'))


@app.route('/logout/')
def logout():
    if session.get('username') is not None:
        session['username'] = None
        session['acc_type'] = None
        return redirect(url_for('mainPage'))
    else:
        return redirect(url_for('not_found'))


@app.route('/dashboard/')
def dashboard():
    if session.get('username') is not None:
        if session.get('acc_type') == 'master':
            return redirect(url_for('postEvent'))
        else:
            user = Session.query(UserProfiles).filter_by(
                username=session.get('username')).one()
            return render_template('dashboard/dashboard.html', user=user,
                                   logged=session.get('username'),
                                   acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('not_found'))


@app.route('/post_event/', methods=['GET', 'POST'])
def postEvent():
    if session.get('username') is not None:
        if request.method == 'POST':
            event = Events(title=request.form['title'],
                           type=request.form['type'],
                           starts=request.form['starts'],
                           ends=request.form['ends'],
                           description=request.form['description'],
                           club=request.form['club'],
                           post_date=datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                           head=request.form['head'])
            user = Session.query(UserAccounts).filter_by(
                username=event.head).one()
            if not user.acc_type == 'master':
                user.acc_type = 'eventhead'
            Session.add(event)
            Session.add(user)
            Session.commit()
            ufile = request.files['image']
            filename = 'static/uploads/' + str(event.id) + '.jpg'
            ufile.save(filename)
            return redirect(url_for('eventInfo', event_id=event.id))
        else:
            users = Session.query(UserAccounts).all()
            return render_template('dashboard/post_event.html',
                                   logged=session.get('username'), users=users,
                                   acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('not_found'))


@app.route('/permission/', methods=['GET', 'POST'])
def permission():
    if session.get('username') is not None:
        if request.method == 'POST':
            user = Session.query(UserAccounts).filter_by(
                username=request.form['username']).one()
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
        return redirect(url_for('not_found'))


@app.route('/edit_profile/', methods=['GET', 'POST'])
def editProfile():
    if session.get('username') is not None:
        profile = Session.query(UserProfiles).filter_by(
            username=session.get('username')).one()
        if request.method == 'POST':
            profile.f_name = request.form['f_name']
            profile.l_name = request.form['l_name']
            profile.dob = request.form['dob']
            profile.mobile = request.form['mobile']
            profile.gender = request.form['gender']
            profile.rollno = request.form['rollno']
            profile.email = request.form['email']
            Session.add(profile)
            Session.commit()
            return redirect(url_for('editProfile'))
        else:
            return render_template('dashboard/edit_profile.html',
                                   logged=session.get('username'),
                                   profile=profile,
                                   acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('not_found'))


@app.route('/view_profile/<username>')
def viewProfile(username):
    if session.get('username') is not None:
        user = Session.query(UserProfiles).filter_by(username=username).one()
        return render_template('dashboard/view_profile.html', user=user,
                               logged=session.get('username'),
                               acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('not_found'))


@app.route('/manage_events/')
def manageEvents():
    if session.get('username') is not None:
        events = Session.query(Events).filter_by(
            head=session.get('username')).all()
        return render_template('dashboard/manage_events.html', events=events,
                               logged=session.get('username'),
                               acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('not_found'))


@app.route('/<int:event_id>/create_team/', methods=['GET', 'POST'])
def createTeam(event_id):
    if session.get('username') is not None:
        if request.method == 'POST':
            team_head = Session.query(UserAccounts).filter_by(
                username=request.form['team_head']).one()
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
        return redirect(url_for('not_found'))


@app.route('/manage_teams/')
def manageTeams():
    if session.get('username') is not None:
        teams = Session.query(Teams).filter_by(
            team_head=session.get('username')).all()
        return render_template('dashboard/manage_teams.html', teams=teams,
                               logged=session.get('username'),
                               acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('not_found'))


@app.route('/delete_team/<int:team_id>')
def deleteTeam(team_id):
    if session.get('username') is not None:
        team = Session.query(Teams).filter_by(id=team_id).one()
        Session.delete(team)
        Session.commit()
        return redirect(url_for('manageTeams'))
    else:
        return redirect(url_for('not_found'))


@app.route('/<int:team_id>/team_members/', methods=['GET', 'POST'])
def teamMembers(team_id):
    if session.get('username') is not None:
        if request.method == 'POST':
            member = TeamMembers(team_id=team_id,
                                 member=request.form['username'])
            user = Session.query(UserAccounts).filter_by(
                username=request.form['username']).one()
            user.acc_type = 'member'
            Session.add(member)
            Session.commit()
            return redirect(url_for('teamMembers', team_id=team_id))
        else:
            users = Session.query(UserAccounts).all()
            members = Session.query(TeamMembers).filter_by(
                team_id=team_id).all()
            return render_template('dashboard/team_members.html',
                                   logged=session.get('username'),
                                   acc_type=session.get('acc_type'),
                                   members=members, users=users)
    else:
        return redirect(url_for('not_found'))


@app.route('/remove_member/<int:member_id>')
def removeMember(member_id):
    if session.get('username') is not None:
        member = Session.query(TeamMembers).filter_by(id=member_id).one()
        team_id = member.team_id
        Session.delete(member)
        Session.commit()
        return redirect(url_for('teamMembers', team_id=team_id))
    else:
        return redirect(url_for('not_found'))


@app.route('/<int:event_id>/event_options/')
def eventOptions(event_id):
    if session.get('username') is not None:
        event = Session.query(Events).filter_by(id=event_id).one()
        return render_template('dashboard/event_options.html',
                               logged=session.get('username'), event=event,
                               acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('not_found'))


@app.route('/<int:event_id>/delete_event/')
def deleteEvent(event_id):
    if session.get('username') is not None:
        event = Session.query(Events).filter_by(id=event_id).one()
        filename = 'static/uploads/' + str(event.id) + '.jpg'
        os.remove(filename)
        Session.delete(event)
        Session.commit()
        return redirect(url_for('manageEvents'))
    else:
        return redirect(url_for('not_found'))


@app.route('/<int:event_id>/edit_event/', methods=['GET', 'POST'])
def editEvent(event_id):
    if session.get('username') is not None:
        event = Session.query(Events).filter_by(id=event_id).one()
        if request.method == 'POST':
            event.title = request.form['title']
            event.type = request.form['type']
            event.starts = request.form['starts']
            event.ends = request.form['ends']
            event.description = request.form['description']
            event.contact = request.form['contact']
            event.club = request.form['club']
            if request.files['image']:
                ufile = request.files['image']
                filename = 'static/uploads/' + str(event.id) + '.jpg'
                ufile.save(filename)
            Session.add(event)
            Session.commit()
            return redirect(url_for('eventOptions', event_id=event_id))
        else:
            return render_template('dashboard/edit_event.html',
                                   logged=session.get('username'),
                                   event=event,
                                   acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('not_found'))


@app.route('/send_message/', methods=['GET', 'POST'])
def sendMessage():
    if session.get('username') is not None:
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
            users = Session.query(UserAccounts).filter_by(
                acc_type='master').all()
            return render_template('dashboard/message.html',
                                   logged=session.get('username'), users=users,
                                   acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('not_found'))


@app.route('/inbox/')
def inbox():
    if session.get('username') is not None:
        messages = Session.query(Messages).filter_by(
            username=session.get('username')).all()
        return render_template('dashboard/inbox.html',
                               logged=session.get('username'),
                               messages=messages,
                               acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('not_found'))


@app.route('/delete_message/<int:message_id>')
def deleteMessage(message_id):
    if session.get('username') is not None:
        message = Session.query(Messages).filter_by(id=message_id).one()
        Session.delete(message)
        Session.commit()
        return redirect(url_for('inbox'))
    else:
        return redirect(url_for('not_found'))


@app.route('/<int:team_id>/team_list/', methods=['GET', 'POST'])
def teamList(team_id):
    if session.get('username') is not None:
        if request.method == 'POST':
            item = ListItems(item=request.form['item'], team_id=team_id)
            Session.add(item)
            Session.commit()
            return redirect(url_for('teamList', team_id=team_id))
        else:
            team = Session.query(Teams).filter_by(id=team_id).one()
            items = Session.query(ListItems).filter_by(team_id=team_id).all()
            return render_template('dashboard/team_list.html',
                                   logged=session.get('username'),
                                   acc_type=session.get('acc_type'),
                                   items=items, team=team)
    else:
        return redirect(url_for('not_found'))


@app.route('/delete_list_item/<int:item_id>')
def deleteItem(item_id):
    if session.get('username') is not None:
        item = Session.query(ListItems).filter_by(id=item_id).one()
        team_id = item.team_id
        Session.delete(item)
        Session.commit()
        return redirect(url_for('teamList', team_id=team_id))
    else:
        return redirect(url_for('not_found'))


@app.route('/<int:team_id>/message/', methods=['GET', 'POST'])
def teamMessage(team_id):
    if session.get('username') is not None:
        if request.method == 'POST':
            message = TeamMessages(title=request.form['title'],
                                   message=request.form['message'],
                                   team_id=team_id)
            Session.add(message)
            Session.commit()
            return redirect(url_for('teamMessage', team_id=team_id))
        else:
            team = Session.query(Teams).filter_by(id=team_id).one()
            return render_template('dashboard/team_message.html',
                                   logged=session.get('username'),
                                   acc_type=session.get('acc_type'), team=team)
    else:
        return redirect(url_for('not_found'))


@app.route('/view_list/<int:team_id>')
def viewList(team_id):
    if session.get('username') is not None:
        items = Session.query(ListItems).filter_by(team_id=team_id).all()
        return render_template('dashboard/view_list.html', items=items,
                               logged=session.get('username'),
                               acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('not_found'))


@app.route('/done_item/<int:item_id>')
def doneItem(item_id):
    if session.get('username') is not None:
        item = Session.query(ListItems).filter_by(id=item_id).one()
        item.done = True
        Session.add(item)
        Session.commit()
        return redirect(url_for('viewList', team_id = item.team_id))
    else:
        return redirect(url_for('not_found'))


@app.route('/undone_item/<int:item_id>')
def undoneItem(item_id):
    if session.get('username') is not None:
        item = Session.query(ListItems).filter_by(id=item_id).one()
        item.done = False
        Session.add(item)
        Session.commit()
        return redirect(url_for('viewList', team_id = item.team_id))
    else:
        return redirect(url_for('not_found'))


@app.route('/view_teams/')
def viewTeams():
    if session.get('username') is not None:
        team_ids = Session.query(TeamMembers).filter_by(
            member=session.get('username')).all()
        teams = []
        for team_id in team_ids:
            team = Session.query(Teams).filter_by(id=team_id.team_id).one()
            teams.append(team)
        return render_template('dashboard/view_teams.html', teams=teams,
                               logged=session.get('username'),
                               acc_type=session.get('acc_type'))
    else:
        return redirect(url_for('not_found'))


@app.route('/<int:team_id>/view_members/')
def viewMembers(team_id):
    if session.get('username') is not None:
        members = Session.query(TeamMembers).filter_by(team_id=team_id).all()
        return render_template('dashboard/view_members.html',
                               logged=session.get('username'),
                               acc_type=session.get('acc_type'),
                               members=members)
    else:
        return redirect(url_for('not_found'))


@app.route('/not_found/')
def not_found():
    return render_template('not_found.html')


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
