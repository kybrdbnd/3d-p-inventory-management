from inventory_management import db
from inventory_management.inventory.models import Filament, Figure, FilamentCategory, Query


def estimate_cost(form):
    filament = Filament.query.get(form.get('filament_color'))
    materialUsed = int(form.get('material_used'))
    time = int(form.get('hour'))
    cost = (filament.price_per_gram * materialUsed) + (time * 20)
    return cost


def get_variants_array(variants):
    variantsArray = []
    for variant in variants:
        variantsArray.append((variant['id'], variant['type']))
    return variantsArray


def get_filaments(category=None):
    if category is None:
        filaments = Filament.query.all()
    else:
        filaments = category.filaments
    filamentArray = [(fil.id, fil.name) for fil in filaments]
    return filamentArray


def get_filament_categories():
    filamentCategories = FilamentCategory.query.order_by('name').all()
    filamentCategoryArray = [(cat.id, cat.name) for cat in filamentCategories]
    return filamentCategoryArray


def get_figures():
    figuresArray = []
    figures = Figure.query.order_by('name').all()
    for figure in figures:
        figuresArray.append((figure.id, figure.name))
    return figuresArray


def save_query(form):
    name = form.get('figure_name')
    filamentCategory = FilamentCategory.query.get(form.get('filament_category')).name
    filamentColor = Filament.query.get(form.get('filament_color')).name
    materialUsed = form.get('material_used')
    hour = form.get('hour')
    variant = form.get('variant')
    x_axis = form.get('x_axis')
    y_axis = form.get('y_axis')
    z_axis = form.get('z_axis')
    comment = form.get('comment')
    extras = {
        filamentCategory: {
            filamentColor: {
                'variants': {
                    variant: {
                        'material_used': materialUsed,
                        'time_taken': hour,
                        'dimensions': {
                            'x_axis': x_axis,
                            'y_axis': y_axis,
                            'z_axis': z_axis
                        }
                    }
                }
            }
        }
    }
    query_instance = Query(name=name, comment=comment, extras=extras)
    db.session.add(query_instance)
    db.session.commit()


if __name__ == '__main__':
    pass
