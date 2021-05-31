from flask import render_template, request, jsonify, url_for, redirect, flash
from sqlalchemy import desc

from inventory_management.inventory import inventory
from inventory_management.inventory.controller.categoryController import (create_category, update_category,
                                                                          delete_category)
from inventory_management.inventory.controller.queryController import (estimate_cost,
                                                                       get_filaments, get_filament_categories,
                                                                       save_query, delete_query)
from inventory_management.inventory.forms import QueryForm, CategoryForm
from inventory_management.inventory.models import FilamentType, Filament, Query, Category
from inventory_management.inventory.schema import filaments_schema, category_schema


@inventory.route('/')
def home():
    return render_template('home.html', page='home')


@inventory.route('/<filament_type_id>/filaments')
def get_filament_colors(filament_type_id):
    filamentType = FilamentType.query.get(filament_type_id)
    return jsonify(filaments_schema.dump(filamentType.filaments))


@inventory.route('/query/create', methods=['GET', 'POST'])
def query_create():
    form = QueryForm()
    form.filament_type.choices = get_filament_categories()
    form.filament_color.choices = get_filaments(FilamentType.query.order_by('name').first())
    if request.method == 'GET':
        return render_template('query.html', form=form, page='query')
    elif request.method == 'POST':
        action = request.form.get('action')
        filamentTypeId = request.form.get('filament_type')
        form.filament_color.choices = get_filaments(FilamentType.query.get(filamentTypeId))
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
            flash(f'Your query {queryId} successfully created', 'success')
            return redirect(url_for('inventory_bp.query_home'))


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
        filamentType = FilamentType.query.filter_by(name=category).first()
        form.filament_type.choices = get_filament_categories()
        form.filament_type.data = str(filamentType.id)
        for color, colorValues in values.items():
            filamentColors = get_filaments(filamentType)
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
            filamentCategoryId = request.form.get('filament_type')
            form.filament_color.choices = get_filaments(FilamentType.query.get(filamentCategoryId))
            form.filament_type.data = filamentCategoryId
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


@inventory.route('/categories', methods=['GET'])
def categories_home():
    categories = Category.query.order_by('name').all()
    return render_template('categories_home.html', categories=categories, page='category')


@inventory.route('/categories/<category_id>', methods=['GET', 'POST'])
def category_edit(category_id):
    category = Category.query.get(category_id)
    form = CategoryForm()
    form.category_name.data = category.name
    if request.method == 'POST':
        update_category(category_id, request.form)
        form.category_name.data = category.name
        flash('category updated successfully!!', 'success')
    return render_template('categories_edit.html', form=form, CATEGORY_ID=category.id, page='category')


@inventory.route('/category/create', methods=['GET', 'POST'])
def category_create():
    form = CategoryForm()
    if request.method == 'POST':
        categoryName = create_category(request.form)
        flash(f'Category {categoryName} created successfully!!', 'success')
        return redirect(url_for('inventory_bp.categories_home'))
    return render_template('categories_edit.html', form=form, page='category')


@inventory.route('/category/<category_id>/delete', methods=['POST'])
def category_delete(category_id):
    if request.method == 'POST':
        categoryInstance = Category.query.get(category_id)
        delete_category(categoryInstance)
        flash('Category Successfully deleted!!', 'success')
    return redirect(url_for('inventory_bp.categories_home'))
