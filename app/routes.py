# app/routes.py
from flask import render_template, flash, redirect, url_for, request, Response
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import func, extract
from datetime import datetime
from app import app, db
import csv
from io import StringIO
from app.models import User, Transaction, Category, Budget
from app.forms import (LoginForm, RegistrationForm, TransactionForm, 
                       CategoryForm, ReportForm, ChangePasswordForm)

# app/routes.py

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    form = TransactionForm()
    
    # --- INICIALIZACIÓN DE VARIABLES---
    chart_labels = []
    chart_data = []
    # -------------------------------------------------------------

    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()]
    
    transactions = Transaction.query.filter_by(owner=current_user).order_by(Transaction.date.desc()).all()
    balance = sum(t.amount for t in transactions) if transactions else 0

    # --- LÓGICA PARA EL GRÁFICO ---
    today = datetime.utcnow()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    expense_data = db.session.query(
        Category.name, 
        func.sum(Transaction.amount * -1).label('total_gastado')
    ).join(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.amount < 0,
        Transaction.date >= start_of_month
    ).group_by(Category.name).order_by(func.sum(Transaction.amount).asc()).all()

    if expense_data:
        chart_labels = [item[0] for item in expense_data]
        chart_data = [float(item[1]) for item in expense_data]
        
    # --- LÓGICA PARA PRESUPUESTOS ---
    budgets = Budget.query.filter_by(user_id=current_user.id, year=today.year, month=today.month).all()
    budgets_dict = {b.category_id: b.amount for b in budgets}
    
    expenses_this_month = db.session.query(
        Transaction.category_id,
        func.sum(Transaction.amount).label('total_spent')
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.amount < 0,
        extract('year', Transaction.date) == today.year,
        extract('month', Transaction.date) == today.month
    ).group_by(Transaction.category_id).all()
    
    expenses_dict = {e.category_id: abs(e.total_spent) for e in expenses_this_month}
    
    return render_template('dashboard.html', title='Dashboard', 
                           transactions=transactions, form=form, balance=balance,
                           chart_labels=chart_labels, chart_data=chart_data,
                           budgets=budgets_dict, expenses=expenses_dict)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña inválidos')
            app.logger.warning(f"Failed login attempt for user '{form.username.data}' from IP {request.remote_addr}")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('dashboard'))
    return render_template('login.html', title='Iniciar Sesión', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # NUEVO: Comprobamos el interruptor antes de hacer nada más.
    if not app.config['REGISTRATION_ENABLED']:
        flash('El registro de nuevos usuarios está desactivado.')
        return redirect(url_for('login'))
        
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('¡Felicidades, ahora eres un usuario registrado!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registro', form=form)

@app.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    # Volvemos a cargar las choices por si la validación falla
    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()]

    if form.validate_on_submit():
        # Obtenemos el objeto Categoría completo desde la BBDD
        selected_category = Category.query.get(form.category.data)

        amount = form.amount.data
        # Si la categoría es de tipo 'gasto', hacemos el número negativo
        if selected_category and selected_category.type == 'gasto':
            amount = -abs(amount)
        else: # Si es 'ingreso' nos aseguramos de que sea positivo
            amount = abs(amount)

        # --- LÍNEA CORREGIDA ---
        # En lugar de 'category=', usamos 'category_id=' para guardar solo el ID.
        t = Transaction(description=form.description.data,
                        amount=amount,
                        category_id=selected_category.id, # <-- CORRECCIÓN AQUÍ
                        owner=current_user)
        # --- FIN DE LA CORRECCIÓN ---

        db.session.add(t)
        db.session.commit()
        flash('¡Transacción añadida!')
    else:
        # Si la validación del formulario falla, es útil mostrar los errores.
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error en el campo '{getattr(form, field).label.text}': {error}", 'danger')

    return redirect(url_for('dashboard'))

@app.route('/categories', methods=['GET'])
@login_required
def manage_categories():
    form = CategoryForm()
    # Buscamos las categorías del usuario y las separamos por tipo
    income_categories = Category.query.filter_by(user_id=current_user.id, type='ingreso').order_by(Category.name).all()
    expense_categories = Category.query.filter_by(user_id=current_user.id, type='gasto').order_by(Category.name).all()
    return render_template('manage_categories.html', title='Gestionar Categorías', form=form,
                           income_categories=income_categories, expense_categories=expense_categories)

@app.route('/add_category', methods=['POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        # Comprobar si ya existe una categoría con ese nombre para el usuario
        existing_category = Category.query.filter_by(user_id=current_user.id, name=form.name.data).first()
        if existing_category:
            flash('Ya existe una categoría con ese nombre.', 'warning')
        else:
            new_category = Category(name=form.name.data, type=form.type.data, user_id=current_user.id)
            db.session.add(new_category)
            db.session.commit()
            flash('¡Nueva categoría añadida con éxito!', 'success')
    return redirect(url_for('manage_categories'))

@app.route('/delete_category/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    # Buscamos la categoría asegurándonos de que pertenece al usuario actual
    category_to_delete = Category.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()

    # Buena práctica: Comprobar si la categoría está siendo usada en alguna transacción
    if category_to_delete.transactions:
        flash('No se puede eliminar la categoría porque tiene transacciones asociadas.', 'danger')
        return redirect(url_for('manage_categories'))

    db.session.delete(category_to_delete)
    db.session.commit()
    flash('Categoría eliminada con éxito.', 'success')
    return redirect(url_for('manage_categories'))

@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    # Buscamos la transacción y nos aseguramos de que pertenece al usuario actual
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=current_user.id).first_or_404()
    form = TransactionForm()

    # Rellenamos el desplegable de categorías, como en el dashboard
    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]

    if form.validate_on_submit():
        # Guardamos los datos actualizados
        selected_category = Category.query.get(form.category.data)
        amount = form.amount.data
        if selected_category.type == 'gasto':
            amount = -abs(amount)
        else:
            amount = abs(amount)

        transaction.description = form.description.data
        transaction.amount = amount
        transaction.category_id = selected_category.id
        db.session.commit()
        flash('¡Transacción actualizada con éxito!', 'success')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        # Al cargar la página (GET), rellenamos el formulario con los datos existentes
        form.description.data = transaction.description
        form.amount.data = abs(transaction.amount) # Mostramos siempre el valor en positivo
        form.category.data = transaction.category_id

    return render_template('edit_transaction.html', title='Editar Transacción', form=form)

@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=current_user.id).first_or_404()
    db.session.delete(transaction)
    db.session.commit()
    flash('¡Transacción eliminada!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/reports', methods=['GET'])
@login_required
def reports():
    form = ReportForm()

    # Obtenemos el mes y año de los argumentos de la URL (o usamos los actuales por defecto)
    selected_year = request.args.get('year', datetime.utcnow().year, type=int)
    selected_month = request.args.get('month', datetime.utcnow().month, type=int)

    # Pre-seleccionamos los valores en el formulario para que el usuario vea qué está filtrando
    form.year.data = selected_year
    form.month.data = selected_month

    # Empezamos la consulta base
    query = Transaction.query.filter_by(user_id=current_user.id)

    # Aplicamos los filtros si no se ha seleccionado "Todos" (valor 0)
    if selected_year != 0:
        query = query.filter(extract('year', Transaction.date) == selected_year)
    if selected_month != 0:
        query = query.filter(extract('month', Transaction.date) == selected_month)

    # Ejecutamos la consulta
    transactions = query.order_by(Transaction.date.desc()).all()

    # Calculamos los totales a partir de los resultados filtrados
    total_income = sum(t.amount for t in transactions if t.amount > 0)
    total_expenses = sum(t.amount for t in transactions if t.amount < 0)
    net_savings = total_income + total_expenses

    return render_template('reports.html', title='Informes', form=form,
                           transactions=transactions, total_income=total_income,
                           total_expenses=total_expenses, net_savings=net_savings,
                           selected_year=selected_year, selected_month=selected_month)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # Primero, verificamos que la contraseña actual es correcta
        if not current_user.check_password(form.current_password.data):
            flash('La contraseña actual es incorrecta.', 'danger')
            return redirect(url_for('profile'))
        
        # Si es correcta, actualizamos a la nueva contraseña
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('¡Tu contraseña ha sido actualizada con éxito!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('profile.html', title='Mi Perfil', form=form)

@app.route('/export_csv')
@login_required
def export_csv():
    # Reutilizamos la misma lógica de filtrado de la página de informes
    selected_year = request.args.get('year', type=int)
    selected_month = request.args.get('month', type=int)

    query = Transaction.query.filter_by(user_id=current_user.id)

    if selected_year and selected_year != 0:
        query = query.filter(extract('year', Transaction.date) == selected_year)
    if selected_month and selected_month != 0:
        query = query.filter(extract('month', Transaction.date) == selected_month)

    transactions = query.order_by(Transaction.date.asc()).all()

    # Usamos StringIO para crear el archivo CSV en memoria
    si = StringIO()
    cw = csv.writer(si)

    # Escribimos las cabeceras
    cw.writerow(['Fecha', 'Descripcion', 'Categoria', 'Importe'])

    # Escribimos los datos de las transacciones
    for t in transactions:
        cw.writerow([t.date.strftime('%Y-%m-%d'), t.description, t.category.name, t.amount])

    # Preparamos la respuesta para el navegador
    output = si.getvalue()

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=informe_contabilidad.csv"})

@app.route('/budgets', methods=['GET', 'POST'])
@login_required
def manage_budgets():
    # Por defecto, trabajamos con el mes y año actuales
    year = request.args.get('year', datetime.utcnow().year, type=int)
    month = request.args.get('month', datetime.utcnow().month, type=int)

    if request.method == 'POST':
        # Procesamos el formulario enviado para guardar/actualizar los presupuestos
        for key, value in request.form.items():
            if key.startswith('budget-'):
                category_id = int(key.split('-')[1])
                # Ignoramos si el valor está vacío
                if not value:
                    continue
                
                amount = float(value)
                
                # Buscamos si ya existe un presupuesto para actualizarlo
                budget = Budget.query.filter_by(user_id=current_user.id, category_id=category_id, year=year, month=month).first()
                if budget:
                    budget.amount = amount
                else:
                    # Si no existe, creamos uno nuevo
                    budget = Budget(user_id=current_user.id, category_id=category_id, year=year, month=month, amount=amount)
                    db.session.add(budget)
        db.session.commit()
        flash('Presupuestos actualizados con éxito', 'success')
        return redirect(url_for('manage_budgets', year=year, month=month))

    # Obtenemos solo las categorías de gastos para presupuestar
    expense_categories = Category.query.filter_by(user_id=current_user.id, type='gasto').all()
    
    # Obtenemos los presupuestos existentes para este período
    budgets = Budget.query.filter_by(user_id=current_user.id, year=year, month=month).all()
    # Creamos un diccionario para acceder fácilmente al presupuesto de cada categoría en la plantilla
    budgets_dict = {b.category_id: b.amount for b in budgets}

    return render_template('budgets.html', title='Gestionar Presupuestos', 
                           categories=expense_categories, budgets=budgets_dict,
                           year=year, month=month)
