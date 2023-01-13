from clinic import app
from flask import render_template, redirect, url_for, flash
from clinic.models import Department, User, Appointment
from clinic.forms import RegisterForm, LoginForm, BookingForm
from clinic import db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

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


@app.route('/details/<string:code>')
@login_required
def details_page(code):
    cur_department = Department.query.filter_by(code=code).first()
    appointments = (
        Appointment.query
            .filter_by(department_id=cur_department.id)
            .filter(Appointment.end_time > datetime.now())
            .order_by(Appointment.end_time)
    )
    return render_template('details.html', appointments=appointments, code=code)


@app.route('/booking/<string:code>', methods=['GET', 'POST'])
@login_required
def booking_page(code):
    form = BookingForm()
    if form.validate_on_submit():
        cur_department = Department.query.filter_by(code=code).first()
        if cur_department is None:
            flash(f'Department code {code} does not exists', category='danger')
            return render_template('booking.html', form=form, code=code, time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        department_id = cur_department.id
        appointment_to_create = Appointment(
            user_id=current_user.get_id(),
            client_name=form.client_name.data,
            client_phone=form.client_phone.data,
            department_id=department_id,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            category=form.category.data,
            message=form.message.data
        )
        db.session.add(appointment_to_create)
        db.session.commit()
        flash(f"Appointment booked successfully!", category='success')
        return redirect(url_for('appointment_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error when make appointment: {err_msg}', category='danger')

    start_time = form.start_time.data or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    end_time  = form.end_time.data or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('booking.html', form=form, code=code, start_time=start_time, end_time=end_time)