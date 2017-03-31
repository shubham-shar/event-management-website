import datetime
from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, UserAccounts, UserProfiles, Teams, Lists, ListItems, Messages, TeamMembers, Events, Comments

app = Flask(__name__)

engine = create_engine('sqlite:///event_database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/events/')
def mainPage():
    return render_template('main_page.html')

@app.route('/<event_type>/')
def eventList(event_type):
    events = session.query(Events).filter_by(type=event_type).all()
    return render_template('event_list.html', events=events, event_type=event_type)

@app.route('/<int:event_id>/', methods=['GET', 'POST'])
def eventInfo(event_id):
    if request.method == 'POST':
        add_comment = Comments(comment=request.form['add_comment'], post_date=datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"), event_id=event_id, username="skb1129")
        session.add(add_comment)
        session.commit()
        return redirect(url_for('eventInfo', event_id=event_id))
    else:
        event = session.query(Events).filter_by(id=event_id).one()
        comments = session.query(Comments).filter_by(event_id=event_id).all()
        return render_template('event_info.html', event=event, comments=comments)
    
@app.route('/signup/', methods=['GET', 'POST'])
def signupPage():
    if request.method == 'POST':
        user = UserAccounts(username=request.form['username'], password=request.form['password'])
        session.add(user)
        session.commit()
        profile = UserProfiles(f_name=request.form['f_name'], l_name=request.form['l_name'], dob=request.form['dob'], mobile=request.form['mobile'], gender=request.form['gender'], rollno=request.form['rollno'], username=request.form['username'], email=request.form['email'])
        session.add(profile)
        session.commit()
        return redirect(url_for('mainPage'))
    else:
        return render_template('signup_page.html')
    
@app.route('/login/', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        user = UserAccounts(username=request.form['username'], password=request.form['password'])
        return redirect(url_for('mainPage'))
    else:
        return render_template('login_page.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
