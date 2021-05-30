from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired


class QueryForm(FlaskForm):
    filament_category = SelectField('Choose Filament Type', choices=[])
    filament_color = SelectField('Choose Color', choices=[])
    figure_name = StringField('Name of the figure', [DataRequired()])
    material_used = IntegerField('Estimated material to be used')
    hour = IntegerField('Estimated time to complete the print')
    variant = SelectField('Select Variant', choices=[(1, 'Original'), (2, 'Small'), (3, 'medium')])
    x_axis = IntegerField('Length of the product')
    y_axis = IntegerField('Breadth of the product')
    z_axis = IntegerField('Height of the product')
    comment = TextAreaField('Extra Comments', render_kw={"rows": 5, "cols": 50})
