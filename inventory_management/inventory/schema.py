from inventory_management import ma


class FilamentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


filament_schema = FilamentSchema()
filaments_schema = FilamentSchema(many=True)
