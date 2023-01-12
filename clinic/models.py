from clinic import db, login_manager
from clinic import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    appointments = db.relationship('Appointment', backref='user_in_appointment', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Department(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.String(length=6), nullable=False, unique=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    address = db.Column(db.String(length=64), nullable=False, unique=True)
    appointments = db.relationship('Appointment', backref='dep_in_appointment', lazy=True)

    def __repr__(self) -> str:
        return f"Department {self.name}"


class Appointment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    department_id = db.Column(db.Integer(), db.ForeignKey('department.id'))
    start_time = db.Column(db.Date(), nullable=False)
    end_time = db.Column(db.Date(), nullable=False)
    category = db.Column(db.String(length=32), nullable=False)
    message = db.Column(db.String(length=128))
