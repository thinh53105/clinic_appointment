from clinic import app, db
from clinic.models import Department

with app.app_context():
    db.drop_all()
    db.create_all()
    dep1 = Department(code="hcmc", name="Ho Chi Minh Department", address="Ho Chi Minh City, Vietnam")
    dep2 = Department(code="hanoi", name="Ha Noi Department", address="Ha Noi, Vietnam")
    db.session.add(dep1)
    db.session.add(dep2)
    db.session.commit()
    
    print(Department.query.all())