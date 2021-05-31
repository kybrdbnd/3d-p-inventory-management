from inventory_management import db
from inventory_management.inventory.models import Category


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


if __name__ == '__main__':
    pass
