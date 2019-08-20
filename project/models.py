from project import db

class users(db.Model):
    #id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False, primary_key=True)
    passwd = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "user(name:{}, mailID:{})".format(self.name, self.email)
