from app import db
from hashlib import md5

ROLE_USER = 0
ROLE_ADMIN = 1

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    expenses = db.relationship('Expense', backref = 'owner', lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    
    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    def __repr__(self):
        return '<Owner %r>' % (self.nickname)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(80))
    description = db.Column(db.String(120))
    vendor = db.Column(db.String(80))
    amount = db.Column(db.String(10))
    date = db.Column(db.DateTime)
    mode = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))

    def __repr__(self):
        return '<Expense %r>' % (self.description)

