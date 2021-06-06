from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired


class QueryForm(FlaskForm):
    filament_type = SelectField('Choose Filament Type', choices=[])
    filament_color = SelectField('Choose Color', choices=[])
    figure_name = StringField('Name of the figure', [DataRequired()])
    material_used = IntegerField('Estimated material to be used')
    hour = IntegerField('Estimated time to complete the print')
    variant = SelectField('Select Variant', choices=[(1, 'Original'), (2, 'Small'), (3, 'Medium')])
    x_axis = IntegerField('Length of the product')
    y_axis = IntegerField('Breadth of the product')
    z_axis = IntegerField('Height of the product')
    comment = TextAreaField('Extra Comments', render_kw={"rows": 5, "cols": 50})


class CategoryForm(FlaskForm):
    category_name = StringField('Name of the category', [DataRequired()])


class FilamentTypeForm(FlaskForm):
    filament_type_name = StringField('Name of the filament type', [DataRequired()])


class FilamentColorForm(FlaskForm):
    filament_color = StringField('Name of the filament color', [DataRequired()])
    price_per_gram = IntegerField('Price per gram', [DataRequired()])
    filament_type = SelectField('Choose Filament Type', choices=[])


class VariantForm(FlaskForm):
    figure_size = StringField('Size of the figure')
    figure_name = SelectField('Name of the figure', choices=[])
    filament_type = SelectField('Type of filament used')
    filament_color = SelectField('Color of the filament used')
    comment = TextAreaField('Extra Comments', render_kw={"rows": 5, "cols": 50})
    x_axis = IntegerField('Length of the figure')
    y_axis = IntegerField('Breadth of the figure')
    z_axis = IntegerField('Height of the figure')
    price = IntegerField('Cost of the figure')
    count = IntegerField('Count of the figure')


class FigureForm(FlaskForm):
    figure_name = StringField('Name of the figure', [DataRequired()])
    category = SelectField('Category of the figure', choices=[])


class IdeasForm(FlaskForm):
    name = StringField("Name of the idea", [DataRequired()])
    filament_type = SelectField("Type of the filament", choices=[])
    filament_color = SelectField("Color of the filament", choices=[])
    comment = TextAreaField('Extra Comments', render_kw={"rows": 5, "cols": 50})
    x_axis = IntegerField('Length of the figure')
    y_axis = IntegerField('Breadth of the figure')
    z_axis = IntegerField('Height of the figure')
