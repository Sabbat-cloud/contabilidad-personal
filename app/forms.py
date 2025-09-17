# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from wtforms.fields import DateField
from app.models import User
from datetime import datetime
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password2 = PasswordField(
        'Repetir Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Este nombre de usuario ya está en uso.')

class TransactionForm(FlaskForm):
    description = StringField('Descripción', validators=[DataRequired()])
    amount = DecimalField('Cantidad', validators=[DataRequired()])
    category = SelectField('Categoría', choices=[
        ('Ingreso', 'Ingreso'),
        ('Comida', 'Comida'),
        ('Transporte', 'Transporte'),
        ('Ocio', 'Ocio'),
        ('Hogar', 'Hogar')
    ], validators=[DataRequired()])
    submit = SubmitField('Añadir Transacción')

class CategoryForm(FlaskForm):
    name = StringField('Nombre de la Categoría', validators=[DataRequired()])
    type = SelectField('Tipo', choices=[
        ('gasto', 'Gasto'),
        ('ingreso', 'Ingreso')
    ], validators=[DataRequired()])
    submit = SubmitField('Añadir Categoría')

class ReportForm(FlaskForm):
    # Generamos una lista de años desde el actual hasta 2020
    current_year = datetime.utcnow().year
    years = [(y, str(y)) for y in range(current_year, 2019, -1)]
    # Añadimos una opción para ver todos los años
    years.insert(0, (0, 'Todos'))

    # Creamos la lista de meses
    months = [
        (0, 'Todos'), (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
        (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
        (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
    ]

    year = SelectField('Año', choices=years, coerce=int)
    month = SelectField('Mes', choices=months, coerce=int)
    submit = SubmitField('Generar Informe')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Contraseña Actual', validators=[DataRequired()])
    new_password = PasswordField('Nueva Contraseña', validators=[DataRequired()])
    new_password2 = PasswordField(
        'Repetir Nueva Contraseña', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Cambiar Contraseña')

class RecurringTransactionForm(FlaskForm):
    description = StringField('Descripción', validators=[DataRequired()])
    amount = DecimalField('Cantidad', validators=[DataRequired()])
    category = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    frequency = SelectField('Frecuencia', choices=[
        ('monthly', 'Mensual'),
        ('weekly', 'Semanal'),
        ('yearly', 'Anual')
    ], validators=[DataRequired()])
    start_date = DateField('Fecha de Inicio', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Guardar Transacción Recurrente')
