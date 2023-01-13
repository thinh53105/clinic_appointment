from clinic import app, db
from clinic.models import Department, User, Appointment
from datetime import datetime, timedelta

with app.app_context():
    db.drop_all()
    db.create_all()
    dep1 = Department(code="hcmc", name="Ho Chi Minh Department", address="Ho Chi Minh City, Vietnam")
    dep2 = Department(code="hanoi", name="Ha Noi Department", address="Ha Noi, Vietnam")
    db.session.add(dep1)
    db.session.add(dep2)
    db.session.commit()
    user1 = User(username='fake1', email_address='fake1@fake.com', password_hash='a')
    user2 = User(username='fake2', email_address='fake2@fake.com', password_hash='b')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    
    t = datetime.now()
    app_list = [
        Appointment(
            user_id=user1.id, department_id=dep1.id, 
            client_name='Thinh', client_phone='0123456789',
            start_time=t, end_time=t + timedelta(hours=1),
            category='health_check', message= 'Health check monthly'
        ),
        Appointment(
            user_id=user2.id, department_id=dep1.id, 
            client_name='Bao', client_phone='0123456798',
            start_time=t + timedelta(hours=4), end_time=t + timedelta(hours=5, minutes=30),
            category='beauty', message= 'Rhinoplasty'
        ),
        Appointment(
            user_id=user2.id, department_id=dep1.id, 
            client_name='Trong', client_phone='0999999999',
            start_time=t + timedelta(hours=8), end_time=t + timedelta(hours=8, minutes=30),
            category='health_check', message= 'Health check monthly'
        ),
        Appointment(
            user_id=user1.id, department_id=dep1.id, 
            client_name='Dai', client_phone='0999999998',
            start_time=t + timedelta(hours=11), end_time=t + timedelta(hours=13, minutes=30),
            category='foot', message= 'Foot Cast'
        ),
        Appointment(
            user_id=user1.id, department_id=dep2.id, 
            client_name='Khanh', client_phone='0999999789',
            start_time=t + timedelta(hours=1), end_time=t + timedelta(hours=2),
            category='foot', message= 'Foot Cast'
        )
    ]
    for app in app_list:
        db.session.add(app)
    db.session.commit()
    
    print(Appointment.query.all())