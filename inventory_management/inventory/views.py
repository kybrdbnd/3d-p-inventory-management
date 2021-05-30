from flask import render_template, request, jsonify, url_for, redirect, flash
from sqlalchemy import desc

from inventory_management.inventory import inventory
from inventory_management.inventory.controller.queryController import (estimate_cost,
                                                                       get_filaments, get_filament_categories,
                                                                       save_query, delete_query)
from inventory_management.inventory.forms import QueryForm
from inventory_management.inventory.models import Figure, FilamentCategory, Filament, Query
from inventory_management.inventory.schema import filaments_schema


@inventory.route('/')
def home():
    return render_template('home.html', page='home')


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
        return render_template('query.html', form=form, page='query')
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
            }, page='query')
        if action == 'save':
            queryId = save_query(request.form)
            flash('Your query successfully created', 'success')
            return redirect(url_for('inventory_bp.query_edit', query_no=queryId))


@inventory.route('/query', methods=['GET', 'POST'])
def query_home():
    queries = Query.query.order_by(desc('created_on')).all()
    return render_template('query_home.html', queries=queries, page='query')


@inventory.route('/query/<query_no>', methods=['GET', 'POST'])
def query_edit(query_no):
    customerQuery = Query.query.filter_by(query_id=query_no).first()
    form = QueryForm()
    form.figure_name.data = customerQuery.name
    for category, values in customerQuery.extras.items():
        filamentCategory = FilamentCategory.query.filter_by(name=category).first()
        form.filament_category.choices = get_filament_categories()
        form.filament_category.data = str(filamentCategory.id)
        for color, colorValues in values.items():
            filamentColors = get_filaments(filamentCategory)
            filament = list(filter(lambda x: x[1] == color, filamentColors))[0]
            form.filament_color.choices = filamentColors
            form.filament_color.data = str(filament[0])
            variants = colorValues['variants']
            for variant, variantValues in variants.items():
                form.variant.data = variant
                form.material_used.data = variantValues['material_used']
                form.hour.data = variantValues['time_taken']
                form.comment.data = variantValues['comments']
                dimensions = variantValues['dimensions']
                form.x_axis.data = dimensions['x_axis']
                form.y_axis.data = dimensions['y_axis']
                form.z_axis.data = dimensions['z_axis']
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'cost':
            filament = Filament.query.get(request.form.get('filament_color'))
            pricePerGram = filament.price_per_gram
            estimatedCost = estimate_cost(request.form)
            return render_template('query.html', form=form, QUERY_ID=query_no, data={
                'estimated_cost': estimatedCost,
                'price_per_gram': pricePerGram
            }, page='query')
        if action == 'update':
            filamentCategoryId = request.form.get('filament_category')
            form.filament_color.choices = get_filaments(FilamentCategory.query.get(filamentCategoryId))
            form.filament_category.data = filamentCategoryId
            form.filament_color.data = request.form.get('filament_color')
            form.variant.data = request.form.get('variant')
            save_query(request.form, query_no)
            flash('Your query successfully updated', 'success')
    return render_template('query.html', form=form, QUERY_ID=query_no, page='query')


@inventory.route('/query/<query_no>/delete', methods=['POST'])
def delete_query_instance(query_no):
    if request.method == 'POST':
        queryInstance = Query.query.filter_by(query_id=query_no).first()
        delete_query(queryInstance)
        flash('Query Successfully deleted!!', 'success')
    return redirect(url_for('inventory_bp.query_home'))
