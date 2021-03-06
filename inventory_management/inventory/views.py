from flask import render_template, request, jsonify, url_for, redirect, flash
from sqlalchemy import desc

from inventory_management.inventory import inventory
from inventory_management.inventory.controller.categoryController import (create_category, update_category,
                                                                          delete_category, get_categories,
                                                                          create_figure, create_variant, update_variant,
                                                                          delete_figure, delete_variant)
from inventory_management.inventory.controller.filamentController import (create_filament_type, delete_filament_type,
                                                                          update_filament_type, create_filament_color,
                                                                          update_filament_color, delete_filament_color)
from inventory_management.inventory.controller.ideasController import create_ideas, update_idea, delete_idea
from inventory_management.inventory.controller.queryController import (estimate_cost,
                                                                       get_filaments, get_filament_types,
                                                                       save_query, delete_query, get_figures)
from inventory_management.inventory.forms import QueryForm, CategoryForm, FilamentTypeForm, FilamentColorForm, \
    FigureForm, VariantForm, IdeasForm
from inventory_management.inventory.models import FilamentType, Filament, Query, Category, Variant, Figure, Idea
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
    form.filament_type.choices = get_filament_types()
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
        form.filament_type.choices = get_filament_types()
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
    figures = Figure.query.order_by('name').all()
    return render_template('categories_home.html', categories=categories, figures=figures, page='category')


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


@inventory.route('/filament_types', methods=['GET'])
def filament_home():
    filamentTypes = FilamentType.query.order_by('name').all()
    filamentColors = Filament.query.order_by('name').all()
    return render_template('filament_home.html', filamentTypes=filamentTypes, filamentColors=filamentColors,
                           page='filament')


@inventory.route('/filament_type/<filament_type_id>', methods=['GET', 'POST'])
def filament_type_edit(filament_type_id):
    filamentType = FilamentType.query.get(filament_type_id)
    form = FilamentTypeForm()
    form.filament_type_name.data = filamentType.name
    if request.method == 'POST':
        update_filament_type(filament_type_id, request.form)
        form.filament_type_name.data = filamentType.name
        flash('filament type updated successfully!!', 'success')
    return render_template('filament_edit.html', form=form, FILAMENT_TYPE_ID=filamentType.id, page='filament')


@inventory.route('/filament_type/create', methods=['GET', 'POST'])
def filament_type_create():
    form = FilamentTypeForm()
    if request.method == 'POST':
        filamentTypeName = create_filament_type(request.form)
        flash(f'Filament type {filamentTypeName} created successfully!!', 'success')
        return redirect(url_for('inventory_bp.filament_home'))
    return render_template('filament_edit.html', form=form, page='filament')


@inventory.route('/filament_type/<filament_type_id>/delete', methods=['POST'])
def filament_type_delete(filament_type_id):
    if request.method == 'POST':
        filamentTypeInstance = FilamentType.query.get(filament_type_id)
        delete_filament_type(filamentTypeInstance)
        flash('Filament Type Successfully deleted!!', 'success')
    return redirect(url_for('inventory_bp.filament_home'))


@inventory.route('/filament_color/create', methods=['GET', 'POST'])
def filament_color_create():
    form = FilamentColorForm()
    form.filament_type.choices = get_filament_types()
    if request.method == 'POST':
        create_filament_color(request.form)
        flash('Filament color created successfully', 'success')
        return redirect(url_for('inventory_bp.filament_home'))
    return render_template('filament_color_edit.html', form=form, page='filament')


@inventory.route('/filament_color/<filament_color_id>', methods=['GET', 'POST'])
def filament_color_edit(filament_color_id):
    filamentInstance = Filament.query.get(filament_color_id)
    form = FilamentColorForm()
    filamentTypes = get_filament_types()
    form.filament_type.choices = filamentTypes
    form.price_per_gram.data = filamentInstance.price_per_gram
    form.filament_type.data = str(filamentInstance.filament_type.id)
    form.filament_color.data = filamentInstance.name
    if request.method == 'POST':
        update_filament_color(filament_color_id, request.form)
        form.filament_color.data = filamentInstance.name
        form.filament_type.data = str(filamentInstance.filament_type.id)
        flash('filament color updated successfully!!', 'success')
    return render_template('filament_color_edit.html', form=form, FILAMENT_COLOR_ID=filamentInstance.id,
                           page='filament')


@inventory.route('/filament_color/<filament_color_id>/delete', methods=['POST'])
def filament_color_delete(filament_color_id):
    if request.method == 'POST':
        filamentColorInstance = Filament.query.get(filament_color_id)
        delete_filament_color(filamentColorInstance)
        flash('Filament Color Successfully deleted!!', 'success')
    return redirect(url_for('inventory_bp.filament_home'))


@inventory.route('/figure/create', methods=['GET', 'POST'])
def figure_create():
    form = FigureForm()
    form.category.choices = get_categories()
    if request.method == 'POST':
        create_figure(request.form)
        flash('figure created successfully', 'success')
        return redirect(url_for('inventory_bp.categories_home'))
    return render_template('figure_edit.html', form=form, page='category')


@inventory.route('/figure/<figure_id>/delete', methods=['POST'])
def figure_delete(figure_id):
    figureInstance = Figure.query.get(figure_id)
    delete_figure(figureInstance)
    flash('figure successfully deleted', 'success')
    return redirect(url_for('inventory_bp.categories_home'))


@inventory.route('/figure/<figure_id>/variant/create', methods=['GET', 'POST'])
def variant_create(figure_id):
    form = VariantForm()
    form.figure_name.choices = get_figures()
    form.figure_name.data = str(figure_id)
    form.filament_type.choices = get_filament_types()
    form.filament_color.choices = get_filaments(FilamentType.query.order_by('name').first())
    if request.method == 'POST':
        create_variant(request.form, figure_id)
        flash('variant created successfully', 'success')
        return redirect(url_for('inventory_bp.categories_home'))
    return render_template('variant_edit.html', form=form, page='category', FIGURE_ID=figure_id)


@inventory.route('/figure/<figure_id>/variant/<variant_id>', methods=['GET', 'POST'])
def variant_edit(figure_id, variant_id):
    form = VariantForm()
    form.figure_name.choices = get_figures()
    form.figure_name.data = str(figure_id)
    variantInstance = Variant.query.get(variant_id)
    form.filament_type.choices = get_filament_types()
    form.filament_type.data = str(variantInstance.filament_type)
    form.filament_color.choices = [(color['id'], color['name']) for color in
                                   get_filament_colors(variantInstance.filament_type.id).json]
    form.figure_size.data = variantInstance.size
    form.price.data = variantInstance.price
    form.count.data = variantInstance.count
    form.comment.data = variantInstance.comments
    dimensions = variantInstance.dimensions
    form.x_axis.data = dimensions['x_axis']
    form.y_axis.data = dimensions['y_axis']
    form.z_axis.data = dimensions['z_axis']
    if request.method == 'POST':
        update_variant(request.form, variant_id)
        form = VariantForm(request.form)
        form.figure_name.choices = get_figures()
        form.filament_type.choices = get_filament_types()
        form.filament_color.choices = [(color['id'], color['name']) for color in
                                       get_filament_colors(int(form.filament_type.data)).json]
        flash('variant updated successfully', 'success')
    return render_template('variant_edit.html', form=form, page='category', VARIANT_ID=variant_id,
                           FIGURE_ID=figure_id)


@inventory.route('/variant/<variant_id>/delete', methods=['POST'])
def variant_delete(variant_id):
    variantInstance = Variant.query.get(variant_id)
    delete_variant(variantInstance)
    flash('variant deleted successfully', 'success')
    return redirect(url_for('inventory_bp.categories_home'))


@inventory.route('/ideas')
def ideas_home():
    ideas = Idea.query.all()
    return render_template('ideas_home.html', ideas=ideas, page='ideas')


@inventory.route('/ideas/create', methods=['GET', 'POST'])
def ideas_create():
    form = IdeasForm()
    form.filament_type.choices = get_filament_types()
    form.filament_color.choices = get_filaments(FilamentType.query.order_by('name').first())
    if request.method == 'POST':
        create_ideas(request.form)
        flash('Idea created successfully', 'success')
        return redirect(url_for('inventory_bp.ideas_home'))
    return render_template('ideas_edit.html', form=form, page='ideas')


@inventory.route('/ideas/<idea_id>', methods=['GET', 'POST'])
def ideas_edit(idea_id):
    ideaInstance = Idea.query.get(idea_id)
    form = IdeasForm()
    form.name.data = ideaInstance.name
    form.filament_type.choices = get_filament_types()
    form.filament_type.data = str(ideaInstance.filament_type.id)
    form.filament_color.choices = get_filaments(ideaInstance.filament_type)
    form.filament_color.data = str(ideaInstance.filament_color.id)
    form.comment.data = ideaInstance.comments
    dimension = ideaInstance.dimensions
    form.x_axis.data = dimension['x_axis']
    form.y_axis.data = dimension['y_axis']
    form.z_axis.data = dimension['z_axis']
    if request.method == 'POST':
        update_idea(idea_id, request.form)
        form = IdeasForm(request.form)
        form.filament_type.choices = get_filament_types()
        form.filament_color.choices = get_filaments(FilamentType.query.get(request.form.get('filament_type')))
        flash("idea updated successfully", "success")
    return render_template('ideas_edit.html', form=form, IDEA_ID=idea_id, page='ideas')


@inventory.route('/ideas/<idea_id>/delete', methods=['POST'])
def ideas_delete(idea_id):
    ideaInstance = Idea.query.get(idea_id)
    delete_idea(ideaInstance)
    flash("idea deleted successfully", "success")
    return redirect(url_for('inventory_bp.ideas_home'))
