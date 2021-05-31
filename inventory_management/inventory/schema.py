from inventory_management import ma


class FilamentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


class QuerySchema(ma.Schema):
    class Meta:
        fields = ('id', 'query_id', 'name', 'created_on', 'comment')


class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


filament_schema = FilamentSchema()
filaments_schema = FilamentSchema(many=True)

query_schema = QuerySchema()
queries_schema = QuerySchema(many=True)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
