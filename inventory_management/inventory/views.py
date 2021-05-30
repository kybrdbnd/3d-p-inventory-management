from flask import render_template, request, jsonify

from inventory_management.inventory import inventory
from inventory_management.inventory.controller.costingController import estimate_cost, get_variants_array, get_figures, \
    get_filaments
from inventory_management.inventory.forms import CostEstimation, QueryForm
from inventory_management.inventory.models import Figure


@inventory.route('/')
def home():
    return render_template('home.html')


@inventory.route('/cost', methods=['GET', 'POST'])
def cost():
    form = CostEstimation()
    form.figure.choices = get_figures()
    form.filament.choices = get_filaments()
    if request.method == 'GET':
        firstFigure = Figure.query.order_by('name').first()
        form.variant.choices = get_variants_array(firstFigure.extras['variants'])  # this is the default variant
        return render_template('cost.html', form=form)
    elif request.method == 'POST':
        filamentId = request.form.get('filament')
        materialUsed = request.form.get('material_used', None)
        hour = request.form.get('hour')
        figureId = request.form.get('figure')
        variant = request.form.get('variant')
        figure = Figure.query.get(figureId)
        form.variant.choices = get_variants_array(figure.extras['variants'])  # this is the default variant
        estimatedCost = estimate_cost(filamentId, hour, materialUsed, figureId, variant)
        return render_template('cost.html', form=form, estimatedCost=estimatedCost)


@inventory.route('/<figureId>/variants')
def get_variants(figureId):
    figure = Figure.query.get(figureId)
    variants = figure.extras['variants']
    return jsonify(variants)


@inventory.route('/query/create')
def query_create():
    form = QueryForm()
    return render_template('query.html', form=form)
