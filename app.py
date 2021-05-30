from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap

from inventory_management import db, app
from inventory_management.inventory.models import Category, Item, Customer, Order, Figure, FilamentCategory

if __name__ == "__main__":
    admin = Admin(app, name='Employee Management', template_mode='bootstrap3')
    admin.add_view(ModelView(FilamentCategory, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Item, db.session))
    admin.add_view(ModelView(Customer, db.session))
    admin.add_view(ModelView(Order, db.session))
    admin.add_view(ModelView(Figure, db.session))

    app.run()
