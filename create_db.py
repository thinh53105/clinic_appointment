from market import app, db
from market.models import Item

with app.app_context():
    db.drop_all()
    db.create_all()
    item1 = Item(name="Iphone10", price=500, barcode="123", description="Iphone 10 haha")
    db.session.add(item1)
    db.session.commit()
    
    print(Item.query.all())