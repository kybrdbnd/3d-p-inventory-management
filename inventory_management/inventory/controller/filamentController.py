from inventory_management import db
from inventory_management.inventory.models import FilamentType, Filament


def create_filament_type(data):
    filamentTypeName = data.get('filament_type_name')
    filamentTypeInstance = FilamentType(name=filamentTypeName)
    db.session.add(filamentTypeInstance)
    db.session.commit()
    return filamentTypeName


def update_filament_type(filament_type_id, data):
    filamentTypeInstance = FilamentType.query.get(filament_type_id)
    filamentTypeName = data.get('filament_type_name')
    filamentTypeInstance.name = filamentTypeName
    db.session.commit()


def delete_filament_type(instance):
    db.session.delete(instance)
    db.session.commit()


def create_filament_color(data):
    filamentColorName = data.get('filament_color')
    pricePerGram = data.get('price_per_gram')
    filamentType = FilamentType.query.get(data.get('filament_type'))
    filamentColorInstance = Filament(name=filamentColorName, price_per_gram=pricePerGram, filament_type=filamentType)
    db.session.add(filamentColorInstance)
    db.session.commit()


def update_filament_color(filament_color_id, data):
    filamentInstance = Filament.query.get(filament_color_id)
    filamentName = data.get('filament_color')
    filamentType = FilamentType.query.get(data.get('filament_type'))
    pricePerGram = data.get('price_per_gram')
    filamentInstance.name = filamentName
    filamentInstance.price_per_gram = pricePerGram
    filamentInstance.filament_type = filamentType
    db.session.commit()


def delete_filament_color(instance):
    db.session.delete(instance)
    db.session.commit()


if __name__ == '__main__':
    pass
