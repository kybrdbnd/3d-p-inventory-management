from inventory_management import db
from inventory_management.inventory.models import Category, FilamentType, Filament, Figure, Variant


def get_categories():
    categories = Category.query.order_by('name').all()
    categoriesArray = [(cat.id, cat.name) for cat in categories]
    return categoriesArray


def create_category(data):
    categoryName = data.get('category_name')
    categoryInstance = Category(name=categoryName)
    db.session.add(categoryInstance)
    db.session.commit()
    return categoryName


def update_category(category_id, data):
    categoryInstance = Category.query.get(category_id)
    categoryName = data.get('category_name')
    categoryInstance.name = categoryName
    db.session.commit()


def delete_category(instance):
    db.session.delete(instance)
    db.session.commit()


def create_figure(data):
    figureName = data.get('figure_name')
    figureSize = data.get('figure_size')
    category = Category.query.get(data.get('category'))
    price = data.get('price')
    count = data.get('count')
    filamentType = FilamentType.query.get(data.get('filament_type'))
    filamentColor = Filament.query.get(data.get('filament_color'))
    comment = data.get('comment')
    dimensions = {
        'x_axis': data.get('x_axis'),
        'y_axis': data.get('y_axis'),
        'z_axis': data.get('z_axis')
    }
    figureInstance = Figure(name=figureName, category=category)
    variantInstance = Variant(size=figureSize, filament_type=filamentType, filament_color=filamentColor, count=count,
                              price=price, comments=comment, dimensions=dimensions)
    figureInstance.variants.append(variantInstance)
    db.session.add_all([figureInstance, variantInstance])
    db.session.commit()


if __name__ == '__main__':
    pass
