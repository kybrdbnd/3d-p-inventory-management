from inventory_management.inventory.models import Filament, Figure


def estimate_cost(filamentId, hours, material_estimated, figureId, variantId):
    filament = Filament.query.get(filamentId)
    if material_estimated != '':
        cost = (int(filament.price_per_gram) * int(material_estimated)) + (int(hours) * 20)
    else:
        figure = Figure.query.get(figureId)
        variants = figure.extras['variants']
        variant = list(filter(lambda x: x['id'] == int(variantId), variants))[0]
        cost = (int(filament.price_per_gram) * variant['material']) + (int(hours) * 20)
    return cost


def get_variants_array(variants):
    variantsArray = []
    for variant in variants:
        variantsArray.append((variant['id'], variant['type']))
    return variantsArray


def get_filaments():
    filamentArray = []
    filaments = Filament.query.all()
    for filament in filaments:
        filamentArray.append((filament.id, filament.name))
    return filamentArray


def get_figures():
    figuresArray = []
    figures = Figure.query.order_by('name').all()
    for figure in figures:
        figuresArray.append((figure.id, figure.name))
    return figuresArray


if __name__ == '__main__':
    pass
