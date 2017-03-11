"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from app import app, db
from flask import render_template, request, redirect, url_for,flash,jsonify
import time
from werkzeug.utils import secure_filename
from forms import ProfileForm
from models import UserProfile
import random


###
# Routing for  application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/profile/',methods=['GET','POST'])   
def profile():
    form = ProfileForm()
    file_folder = app.config['UPLOAD_FOLDER']
    if request.method == "POST" and form.validate_on_submit():
        fname = request.form['firstname']
        lname = request.form['lastname']
        username = request.form['username']
        userid = randomnum()
        age = request.form['age']
        gender = request.form['gender']
        image = request.files['image']
        biography = request.form['biography']
        created=time.strftime("%-d,%b,%Y")
        filename = secure_filename(image.filename)
        image.save(os.path.join(file_folder, filename))
        
        user = UserProfile(fname, lname,username,userid, age, gender,biography,filename,created)
        db.session.add(user) 
        db.session.commit()
        flash ('Profile Created')
        return redirect(url_for('profiles'))
    flash_errors(form)
    return render_template('profileform.html',form=form)

def randomnum():
    ran = random.randrange(82001000, 83006000, 3)
    user = UserProfile.query.filter_by(userid=ran).first()
    #checks if ran is already in the database,if it exists it recalculates ran and returns that value
    if user:
        ran = random.randrange(82001000, 83006000, 7)
        return ran 
    else:
        #if ran does not already exist in the database it returns the original calculate ran
        return ran
    
@app.route('/profile/<userid>',methods=['GET','POST'])
def userprofile(userid):
    """Renders a specific user profile."""
    user = UserProfile.query.filter_by(userid=userid).first()
    if user:
        if request.headers.get('Content-Type') == 'application/json' or request.method == 'POST':
            return jsonify({'userid': user.userid, 'username': user.username, 'image': user.image,'gender':user.gender, 'age': user.age, 'profile_created_on': user.created.strftime("%-d %b %Y")})
        else:
            return render_template('profile.html', fname = user.first_name , lname=user.last_name,created = user.created.strftime("%-d %b %Y"), username = user.username,userid=user.userid, gender = user.gender,age = user.age, img = user.image,biography=user.biography)
    return render_template('NOTEXISTS.HTML')


@app.route('/profiles/',methods=['GET','POST'])
def profiles():
    """Render a list of all user profiles."""
    users = db.session.query(UserProfile).all()
    myuser=[]
    if users:
        for user in users:
            myuser.append({'username': user.username, 'userid': user.userid})
        if request.headers.get('Content-Type') == 'application/json' or request.method == 'POST':
            return jsonify(users=myuser)
    return render_template('profiles.html',users=users) 
    
###
# The functions below should be applicable to all Flask apps.
###
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response
    


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8080)