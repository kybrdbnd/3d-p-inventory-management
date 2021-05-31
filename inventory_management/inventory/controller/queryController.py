from inventory_management import db
from inventory_management.inventory.models import Filament, Figure, FilamentType, Query


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


def get_filament_types():
    filamentTypes = FilamentType.query.order_by('name').all()
    filamentTypesArray = [(cat.id, cat.name) for cat in filamentTypes]
    return filamentTypesArray


def get_figures():
    figuresArray = []
    figures = Figure.query.order_by('name').all()
    for figure in figures:
        figuresArray.append((figure.id, figure.name))
    return figuresArray


def save_query(form, query_no=None):
    name = form.get('figure_name')
    filamentType = FilamentType.query.get(form.get('filament_type')).name
    filamentColor = Filament.query.get(form.get('filament_color')).name
    materialUsed = form.get('material_used')
    hour = form.get('hour')
    variant = form.get('variant')
    x_axis = form.get('x_axis')
    y_axis = form.get('y_axis')
    z_axis = form.get('z_axis')
    comment = form.get('comment')
    extras = {
        filamentType: {
            filamentColor: {
                'variants': {
                    variant: {
                        'material_used': materialUsed,
                        'time_taken': hour,
                        'comments': comment,
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
    if query_no is None:
        queryInstance = Query(name=name, comment=comment, extras=extras)
        db.session.add(queryInstance)
    else:
        queryInstance = Query.query.filter_by(query_id=query_no).first()
        queryInstance.name = name
        queryInstance.comment = comment
        queryInstance.extras = extras
    db.session.commit()
    return queryInstance.query_id


def delete_query(instance):
    db.session.delete(instance)
    db.session.commit()


if __name__ == '__main__':
    pass
