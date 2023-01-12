from clinic import app
from flask import render_template, redirect, url_for, flash
from clinic.models import Department, User, Appointment
from clinic.forms import RegisterForm, LoginForm, BookingForm
from clinic import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/appointment')
@login_required
def appointment_page():
    departments = Department.query.all()
    return render_template('appointment.html', departments=departments)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('appointment_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('appointment_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


@app.route('/booking', methods=['GET', 'POST'])
def booking_page():
    form = BookingForm()
    if form.validate_on_submit():
        appointment_to_create = Appointment(
            user_id=current_user.get_id(),
            department_id=form.department.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data
        )
        db.session.add(appointment_to_create)
        db.session.commit()
        flash(f"Appointment booked successfully!", category='success')
        return redirect(url_for('appointment_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error when make appointment: {err_msg}', category='danger')

    return render_template('booking.html', form=form)