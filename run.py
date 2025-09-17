# run.py
from app import app, db
from app.models import User, Transaction, RecurringTransaction # <-- Importar RecurringTransaction
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import click

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Transaction': Transaction}

# --- NUEVO COMANDO CLI ---
@app.cli.command("process-recurring")
def process_recurring_transactions():
    """Busca y procesa las transacciones recurrentes pendientes."""
    today = date.today()
    # Buscamos transacciones recurrentes cuya próxima fecha de ejecución es hoy o ya ha pasado
    due_transactions = RecurringTransaction.query.filter(RecurringTransaction.next_date <= today).all()

    click.echo(f"Se encontraron {len(due_transactions)} transacciones recurrentes para procesar.")

    for rt in due_transactions:
        # 1. Crear la transacción normal
        new_transaction = Transaction(
            description=rt.description,
            amount=rt.amount,
            date=datetime.combine(rt.next_date, datetime.min.time()),
            category_id=rt.category_id,
            user_id=rt.user_id
        )
        db.session.add(new_transaction)

        # 2. Calcular la siguiente fecha de ejecución
        current_next_date = rt.next_date
        if rt.frequency == 'monthly':
            rt.next_date = current_next_date + relativedelta(months=1)
        elif rt.frequency == 'weekly':
            rt.next_date = current_next_date + relativedelta(weeks=1)
        elif rt.frequency == 'yearly':
            rt.next_date = current_next_date + relativedelta(years=1)

        click.echo(f"Procesada '{rt.description}'. Nueva fecha de ejecución: {rt.next_date.strftime('%Y-%m-%d')}")

    db.session.commit()
    click.echo("Proceso finalizado.")
