from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, FileField, HiddenField
from wtforms.validators import InputRequired
from flask_wtf.file import FileRequired, FileAllowed

class ProfileForm(FlaskForm):
    firstname = StringField('Firstname: ', validators=[InputRequired()])
    lastname = StringField('Lastname: ', validators=[InputRequired()])
    username = StringField('Username: ', validators=[InputRequired()])
    age = IntegerField('Age: ', validators=[InputRequired()])
    gender = SelectField('Gender: ', choices=[('', ''), ('Female', 'Female'),('Male', 'Male')])
    biography = StringField('Biography: ', validators=[InputRequired()])
    image = FileField('Profile Picture: ', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images Only')])
    
