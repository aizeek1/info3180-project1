from . import db

class UserProfile(db.Model):
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    userid = db.Column(db.Integer, unique=True,primary_key=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(6))
    biography = db.Column(db.String(255))
    image = db.Column(db.String(255))
    created = db.Column(db.DateTime())

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
            
    def __init__(self,first_name,last_name, username, userid, age,gender,biography,image,created):
         self.first_name = first_name
         self.last_name = last_name
         self.username = username
         self.userid=userid
         self.age = age
         self.gender = gender
         self.biography = biography
         self.image = image
         self.created= created

    def __repr__(self):
        return '<User %r>' % (self.userid)