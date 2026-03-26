from sales.models import Sale
from finance.models import Expense


def profit_loss():

    sales_total = sum(
        sale.total for sale in Sale.objects.all()
    )

    expenses_total = sum(
        expense.amount for expense in Expense.objects.all()
    )

    profit = sales_total - expenses_total

    return {
        "sales": sales_total,
        "expenses": expenses_total,
        "profit": profit
    }
    