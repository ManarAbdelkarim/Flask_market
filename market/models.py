
from market import db
from market import bcrypt , login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True , unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budgets = db.Column(db.Integer(), nullable=False,default=500)
    items =db.relationship('Item',backref='owner_user',lazy=True)
    def __repr__(self):
        return self.username
    @property
    def password(self):
        return self.password
    @password.setter
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,user_attempted_password):
       return bcrypt.check_password_hash(self.password_hash,user_attempted_password)

    @property
    def prettier_budgets(self):
        if len(str(self.budgets)) >=4:
            return f"{str(self.budgets)[:-3]},{str(self.budgets)[-3:]}"
        else:
            return f"{self.budgets}$"

    def can_purshase(self,object_item):
        return self.budgets >= object_item.price

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True , unique=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer(),nullable=False )
    barcode = db.Column(db.String(length=15),nullable=False , unique=True)
    description = db.Column(db.String(length=1024), nullable=True , unique=True)
    owner= db.Column(db.Integer(),db.ForeignKey('user.id'))

    def __repr__(self):
        return self.name

    def buy(self, current_user):
        self.owner = current_user.id
        current_user.budgets = current_user.budgets - self.price
        db.session.commit()