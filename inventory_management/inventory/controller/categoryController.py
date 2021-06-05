from inventory_management import db
from inventory_management.inventory.models import Category, FilamentType, Filament, Figure, Variant


def get_figures():
    figures = Figure.query.order_by('name').all()
    figuresArray = [(fig.id, fig.name) for fig in figures]
    return figuresArray


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
    category = Category.query.get(data.get('category'))
    figureInstance = Figure(name=figureName, category=category)
    db.session.add(figureInstance)
    db.session.commit()


def delete_figure(instance):
    db.session.delete(instance)
    db.session.commit()


def create_variant(data, figure_id):
    figureInstance = Figure.query.get(figure_id)
    figureSize = data.get('figure_size')
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

    variantInstance = Variant(size=figureSize, filament_type=filamentType, filament_color=filamentColor, count=count,
                              price=price, comments=comment, dimensions=dimensions, figure=figureInstance)
    db.session.add(variantInstance)
    db.session.commit()


def update_variant(data, variant_id):
    variantInstance = Variant.query.get(variant_id)
    variantInstance.size = data.get('figure_size')
    variantInstance.price = data.get('price')
    variantInstance.count = data.get('count')
    variantInstance.filament_type = FilamentType.query.get(data.get('filament_type'))
    variantInstance.filament_color = Filament.query.get(data.get('filament_color'))
    variantInstance.comments = data.get('comment')
    variantInstance.dimensions = {
        'x_axis': data.get('x_axis'),
        'y_axis': data.get('y_axis'),
        'z_axis': data.get('z_axis')
    }
    db.session.commit()


def delete_variant(instance):
    db.session.delete(instance)
    db.session.commit()


if __name__ == '__main__':
    pass
