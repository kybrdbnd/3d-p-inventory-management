from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class CostEstimation(FlaskForm):
    filament = SelectField('Choose Your Filament', choices=[])
    material_used = IntegerField('Enter the estimated material to be used')
    hour = IntegerField('Estimated time to complete the print', [DataRequired()])
    figure = SelectField('Choose Your Figure', choices=[])
    variant = SelectField('Select Variant', choices=[])


class QueryForm(FlaskForm):
    filament_category = SelectField('Choose Filament Type', choices=[])
    filament_color = SelectField('Choose Color', choices=[])
    figure_name = StringField('Name of the figure', [DataRequired()])
    material_used = IntegerField('Estimated material to be used', [DataRequired()])
    hour = IntegerField('Estimated time to complete the print', [DataRequired()])
    variant = SelectField('Select Variant', choices=[(1, 'Original'), (2, 'Small'), (3, 'medium')])
    x_axis = IntegerField('Length of the product', [DataRequired()])
    y_axis = IntegerField('Breadth of the product', [DataRequired()])
    z_axis = IntegerField('Height of the product', [DataRequired()])
    comment = TextAreaField('Extra Comments', render_kw={"rows": 5, "cols": 50})
