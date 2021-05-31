from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from inventory_management import db, app
from inventory_management.inventory.models import (Category, Item, Customer, Order, Figure, FilamentType, Filament,
                                                   Query)

if __name__ == "__main__":
    admin = Admin(app, name='Inventory Management', template_mode='bootstrap3')
    admin.add_view(ModelView(FilamentType, db.session))
    admin.add_view(ModelView(Filament, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Item, db.session))
    admin.add_view(ModelView(Customer, db.session))
    admin.add_view(ModelView(Order, db.session))
    admin.add_view(ModelView(Figure, db.session))
    admin.add_view(ModelView(Query, db.session))

    app.run()
