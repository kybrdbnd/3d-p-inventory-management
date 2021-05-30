from inventory_management.inventory.models import Filament, Figure, FilamentCategory


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


if __name__ == '__main__':
    pass
