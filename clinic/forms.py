from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from clinic.models import User, Appointment
from datetime import datetime, timedelta
from clinic import db
from flask_login import current_user


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class BookingForm(FlaskForm):
    department = StringField(label='Booking Location:', validators=[DataRequired()])
    start_time = DateTimeField(label='Start Time', validators=[DataRequired()])
    end_time = DateTimeField(label='End Time', validators=[DataRequired()])
    category = StringField(label='Category', validators=[DataRequired()])
    message = StringField(label='Message', validators=[DataRequired()])
    submit = SubmitField(label='Submit')
    
    def validate_start_time(self, start_time):
        if start_time.data < datetime.now():
            raise ValidationError('Start time must not be in the past!')
    
    def validate_end_time(self, end_time):
        if end_time.data < datetime.now():
            raise ValidationError('End time must not be in the past!')
    
    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        duration = self.end_time.data - self.start_time.data
        if not (timedelta(minutes=30) <= duration <= timedelta(hours=3)):
            self.end_time.errors.append("Duration must be from 30 minutes to 3 hours")
            return False
        con1 = Appointment.query \
            .filter(Appointment.start_time <= self.start_time.data) \
            .filter(self.start_time.data <= Appointment.end_time).first()
        
        con2 = Appointment.query \
            .filter(Appointment.start_time <= self.end_time.data) \
            .filter(self.end_time.data <= Appointment.end_time).first()
        
        con3 = Appointment.query \
            .filter(Appointment.start_time >= self.end_time.data) \
            .filter(self.end_time.data >= Appointment.end_time).first()
        
        print(con1, con2, con3)
        if any((con1, con2, con3)):
            self.end_time.errors.append("Confict in time, someone already have an appointment is this duration!")
            return False
        return True
    