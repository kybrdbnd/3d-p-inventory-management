from inventory_management import db
from inventory_management.inventory.models import FilamentType, Filament, Idea


def create_ideas(data):
    name = data.get('name')
    filamentType = FilamentType.query.get(data.get('filament_type'))
    filamentColor = Filament.query.get(data.get('filament_color'))
    comments = data.get('comment')
    dimensions = {
        'x_axis': data.get('x_axis'),
        'y_axis': data.get('y_axis'),
        'z_axis': data.get('z_axis')
    }
    ideaInstance = Idea(name=name, filament_type=filamentType, filament_color=filamentColor, comments=comments,
                        dimensions=dimensions)
    db.session.add(ideaInstance)
    db.session.commit()


def update_idea(idea_id, data):
    ideaInstance = Idea.query.get(idea_id)
    ideaInstance.name = data.get('name')
    ideaInstance.filament_type = FilamentType.query.get(data.get('filament_type'))
    ideaInstance.filament_color = Filament.query.get(data.get('filament_color'))
    ideaInstance.comments = data.get('comment')
    ideaInstance.dimensions = {
        'x_axis': data.get('x_axis'),
        'y_axis': data.get('y_axis'),
        'z_axis': data.get('z_axis')
    }
    db.session.commit()


def delete_idea(instance):
    db.session.delete(instance)
    db.session.commit()
