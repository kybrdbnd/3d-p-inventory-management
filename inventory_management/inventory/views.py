from flask import render_template, request, jsonify

from inventory_management.inventory import inventory
from inventory_management.inventory.controller.costingController import estimate_cost, get_variants_array, get_figures, \
    get_filaments, get_filament_categories
from inventory_management.inventory.forms import CostEstimation, QueryForm
from inventory_management.inventory.models import Figure, FilamentCategory, Filament
from inventory_management.inventory.schema import filaments_schema


@inventory.route('/')
def home():
    return render_template('home.html')


@inventory.route('/<filament_category_id>/filaments')
def get_filament_colors(filament_category_id):
    filamentCategory = FilamentCategory.query.get(filament_category_id)
    return jsonify(filaments_schema.dump(filamentCategory.filaments))


@inventory.route('/query/create', methods=['GET', 'POST'])
def query_create():
    form = QueryForm()
    form.filament_category.choices = get_filament_categories()
    form.filament_color.choices = get_filaments(FilamentCategory.query.order_by('name').first())
    if request.method == 'GET':
        return render_template('query.html', form=form)
    elif request.method == 'POST':
        action = request.form.get('action')
        filamentCategoryId = request.form.get('filament_category')
        form.filament_color.choices = get_filaments(FilamentCategory.query.get(filamentCategoryId))

        if action == 'cost':
            filament = Filament.query.get(request.form.get('filament_color'))
            pricePerGram = filament.price_per_gram
            estimatedCost = estimate_cost(request.form)
            return render_template('query.html', form=form, data={
                'estimated_cost': estimatedCost,
                'price_per_gram': pricePerGram
            })
