from inventory_management import ma


class FilamentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


class QuerySchema(ma.Schema):
    class Meta:
        fields = ('id', 'query_id', 'name', 'created_on', 'comment')


filament_schema = FilamentSchema()
filaments_schema = FilamentSchema(many=True)

query_schema = QuerySchema()
queries_schema = QuerySchema(many=True)
