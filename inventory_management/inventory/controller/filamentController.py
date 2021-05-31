from inventory_management import db
from inventory_management.inventory.models import FilamentType


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


if __name__ == '__main__':
    pass
